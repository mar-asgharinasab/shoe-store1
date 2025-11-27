from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.contrib import messages





def cart_detail(request):
    # اطمینان از وجود session برای کاربر مهمان
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # سبد کاربر لاگین‌شده یا مهمان
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)

    cart_items = CartItem.objects.filter(cart=cart).select_related("product")

    # ✅ اعمال تغییرات یا حذف
    if request.method == "POST":
        for key, value in request.POST.items():
            # تغییر تعداد
            if key.startswith("count_"):
                item_id = key.split("_")[1]
                item = get_object_or_404(CartItem, id=item_id, cart=cart)
                new_count = int(value)
                if new_count <= 0:
                    item.delete()
                else:
                    item.count = new_count
                    item.save()
            # حذف آیتم
            elif key.startswith("delete_"):
                item_id = key.split("_")[1]
                CartItem.objects.filter(id=item_id, cart=cart).delete()

        messages.success(request, "✅ تغییرات با موفقیت اعمال شد.")
        return redirect("cart_detail")

    total_price = sum(item.subtotal for item in cart_items)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })


@login_required
def checkout(request):
    # گرفتن سبد خرید فعلی
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart).select_related("product", "color", "size")

    if not cart_items.exists():
        messages.warning(request, "سبد خرید شما خالی است.")
        return redirect("cart_detail")

    if request.method == "POST":
        # اطلاعات خریدار
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal_code")

        # ساخت سفارش
        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            postal_code=postal_code,
        )

        # انتقال همه‌ی آیتم‌های سبد خرید به OrderItem
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                color=item.color,
                size=item.size,
                quantity=item.count,
                price=item.price,
            )

        # خالی کردن سبد خرید بعد از ثبت
        cart_items.delete()
        cart.delete()

        messages.success(request, "✅ سفارش شما با موفقیت ثبت شد. منتظر تماس ادمین باشید.")
        return redirect("order_success")

    return render(request, "cart/checkout.html", {"cart": cart, "cart_items": cart_items})


@login_required
def order_success(request):
    return render(request, "cart/order_success.html")


def added_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "cart/added_to_cart.html", {"product": product})
