from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.views.decorators.http import require_http_methods
import random
import urllib.parse
import urllib.request

from .models import OTPCode


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    مرحله ۱: دریافت شماره موبایل و ارسال کد تأیید
    """
    if request.method == "POST":
        phone = _normalize_phone((request.POST.get('phone') or '').strip())
        if not phone:
            messages.error(request, "شماره موبایل را وارد کنید.")
            return render(request, 'account/login.html')
        if not _is_valid_ir_mobile(phone):
            messages.error(request, "فرمت شماره موبایل معتبر نیست. نمونه صحیح: 09123456789")
            return render(request, 'account/login.html')

        # محدودیت ارسال مجدد
        resend_seconds = getattr(settings, 'KAVENEGAR_OTP_RESEND_SECONDS', 10)
        last_code = OTPCode.objects.filter(phone_number=phone, is_used=False).order_by('-created_at').first()
        if last_code:
            elapsed = (timezone.now() - last_code.created_at).total_seconds()
            remaining_resend = int(resend_seconds - elapsed)
            if remaining_resend > 0:
                messages.warning(request, f"لطفاً {remaining_resend} ثانیه صبر کنید و دوباره تلاش کنید.")
                return render(request, 'account/login.html')

        code = f"{random.randint(100000, 999999)}"
        OTPCode.objects.create(phone_number=phone, code=code)

        ok, err = _send_kavenegar_otp(phone, code)
        if not ok:
            if settings.DEBUG:
                # در حالت توسعه، کد را در پیام‌ها نمایش می‌دهیم
                request.session['otp_phone'] = phone
                messages.warning(
                    request,
                    (err + " | ") if err else "" + f"حالت تست: کد شما {code} است. (در نسخه عملیاتی ارسال پیامک را اصلاح کنید)"
                )
                return redirect('verify')
            messages.error(request, err or "ارسال پیامک با خطا مواجه شد. لطفاً بعداً تلاش کنید.")
            return render(request, 'account/login.html')

        request.session['otp_phone'] = phone
        messages.success(request, f"کد تأیید به شماره {phone} ارسال شد.")
        return redirect('verify')

    return render(request, 'account/login.html')


@require_http_methods(["GET", "POST"])
def verify_view(request):
    """
    مرحله ۲: دریافت کد، اعتبارسنجی و لاگین/ساخت کاربر
    """
    phone = request.session.get('otp_phone')
    expire_seconds = getattr(settings, 'KAVENEGAR_OTP_EXPIRE_SECONDS', 120)
    recent_code = None
    if phone:
        recent_code = OTPCode.objects.filter(phone_number=phone, is_used=False).order_by('-created_at').first()
    remaining = None
    if recent_code:
        elapsed = (timezone.now() - recent_code.created_at).total_seconds()
        remaining = max(0, int(expire_seconds - elapsed))
    debug_code = None
    if settings.DEBUG and recent_code:
        debug_code = recent_code.code

    if request.method == 'POST':
        input_code = (request.POST.get('code') or '').strip()
        phone_post = _normalize_phone((request.POST.get('phone') or '').strip())
        if phone_post:
            phone = phone_post
        if not phone:
            messages.error(request, "ابتدا شماره موبایل را وارد کنید.")
            return redirect('login')
        if not input_code:
            messages.error(request, "کد تأیید را وارد کنید.")
            return render(request, 'account/verify.html', {"phone": phone, "remaining": remaining, "expire_seconds": expire_seconds})

        recent_code = OTPCode.objects.filter(phone_number=phone, is_used=False).order_by('-created_at').first()
        if not recent_code:
            messages.error(request, "کد معتبر یافت نشد. دوباره تلاش کنید.")
            return redirect('login')

        # بررسی انقضا
        if (timezone.now() - recent_code.created_at).total_seconds() > expire_seconds:
            messages.error(request, "اعتبار کد به پایان رسیده است. لطفاً دوباره درخواست دهید.")
            return redirect('login')

        if recent_code.code != input_code:
            messages.error(request, "کد تأیید صحیح نیست.")
            elapsed = (timezone.now() - recent_code.created_at).total_seconds()
            remaining = max(0, int(expire_seconds - elapsed))
            return render(request, 'account/verify.html', {"phone": phone, "remaining": remaining, "expire_seconds": expire_seconds})

        recent_code.is_used = True
        recent_code.save(update_fields=['is_used'])

        user, _ = User.objects.get_or_create(username=phone, defaults={
            'first_name': '',
        })
        login(request, user)
        messages.success(request, "با موفقیت وارد شدید.")
        return redirect('/')

    return render(request, 'account/verify.html', {"phone": phone, "remaining": remaining, "expire_seconds": expire_seconds, "debug_code": debug_code})


def _send_kavenegar_otp(phone: str, code: str):
    api_key = getattr(settings, 'KAVENEGAR_API_KEY', None)
    sender = getattr(settings, 'KAVENEGAR_SENDER', None)
    template = getattr(settings, 'KAVENEGAR_VERIFY_TEMPLATE', '')
    if not api_key:
        return False, "کلید API تنظیم نشده است."

    try:
        from kavenegar import KavenegarAPI  # type: ignore
        api = KavenegarAPI(api_key)
        receptor = _to_international(phone)
        if template:
            api.verify_lookup({
                'receptor': receptor,
                'template': template,
                'token': code,
            })
        else:
            params = {
                'receptor': receptor,
                'message': f"کد ورود شما: {code}",
            }
            if sender:
                params['sender'] = sender
            try:
                api.sms_send(params)
            except Exception as e1:
                if '412' in str(e1):
                    if template:
                        api.verify_lookup({'receptor': receptor, 'template': template, 'token': code})
                    else:
                        api.sms_send({'receptor': receptor, 'message': f"کد ورود شما: {code}"})
                else:
                    raise
        return True, None
    except Exception:
        try:
            receptor = _to_international(phone)
            if template:
                url = f"https://api.kavenegar.com/v1/{api_key}/verify/lookup.json"
                data = {
                    'receptor': receptor,
                    'template': template,
                    'token': code,
                }
            else:
                url = f"https://api.kavenegar.com/v1/{api_key}/sms/send.json"
                data = {
                    'receptor': receptor,
                    'message': f"کد ورود شما: {code}",
                }
                if sender:
                    data['sender'] = sender
            encoded = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data=encoded, method='POST')
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            with urllib.request.urlopen(req, timeout=10) as res:
                res.read()
            return True, None
        except Exception as e2:
            if settings.DEBUG:
                return False, f"خطا در ارسال پیامک: {e2}"
            return False, None


def _normalize_phone(phone: str) -> str:
    if not phone:
        return ''
    persian = '۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩'
    english = '01234567890123456789'
    table = str.maketrans({p: e for p, e in zip(persian, english)})
    p = phone.translate(table)
    p = ''.join(ch for ch in p if ch.isdigit() or ch in ['+', '0'])
    if p.startswith('+98'):
        p = '0' + p[3:]
    elif p.startswith('0098'):
        p = '0' + p[4:]
    elif p.startswith('98'):
        p = '0' + p[2:]
    return p


def _is_valid_ir_mobile(phone: str) -> bool:
    return phone.startswith('09') and len(phone) == 11 and phone.isdigit()


def _to_international(phone: str) -> str:
    p = _normalize_phone(phone)
    if p.startswith('0') and len(p) == 11:
        return '+98' + p[1:]
    if p.startswith('+98'):
        return p
    if p.startswith('98') and len(p) == 12:
        return '+' + p
    return p
