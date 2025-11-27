




# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from django.contrib import messages
# from .models import Product, Comment, Gallary, Color, Size, Category
# from cart.models import Cart, CartItem
# from django.contrib.auth.decorators import login_required


# def category_products(request, category_slug):
#     # دریافت دسته‌بندی بر اساس `slug`
#     category = get_object_or_404(Category, en_title=category_slug)
#     # دریافت تمام محصولات مرتبط با این دسته‌بندی
#     products = Product.objects.filter(categories=category)

#     context = {
#         'category': category,
#         'products': products
#     }
#     return render(request, 'products/category_products.html', context)

# def product_list_view(request):
#     # نمایش لیست محصولات
#     context = {
#         "products": Product.objects.all()
#     }

#     # جستجوی محصولات
#     search = request.POST.get("q")
#     if search:
#         context['products'] = Product.objects.filter(title__icontains=search)

#     return render(request, 'products/products.html', context)


# def product_list_category_view(request, category):
#     # نمایش محصولات بر اساس دسته‌بندی
#     context = {
#         "products": Product.objects.filter(categories__en_title=category),
#         'categories': Category.objects.all()
#     }

#     return render(request, 'products/products.html', context)


# def product_detail_view(request, pk):
#     # دریافت محصول یا نمایش خطای 404 در صورت نبودن
#     product = get_object_or_404(Product, id=pk)
#     comments = Comment.objects.filter(product=product)
#     gallery = Gallary.objects.filter(product=product)
#     colors = product.colors.all()
#     sizes = product.size.all()

#     context = {
#         "product": product,
#         "comments": comments,
#         "gallery": gallery,
#         "colors": colors,
#         "sizes": sizes,
#     }

#     return render(request, 'products/product-detail.html', context)


# # @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     # بررسی موجودی محصول
#     if product.inventory is None or product.inventory <= 0:
#         messages.error(request, "این محصول در انبار موجود نیست.")
#         return redirect('product_detail', pk=product.id)

#     color_id = request.POST.get('color')
#     size_id = request.POST.get('size')
#     quantity = request.POST.get('quantity', 1)

#     try:
#         quantity = int(quantity)
#     except ValueError:
#         messages.error(request, "تعداد وارد شده نامعتبر است.")
#         return redirect('product_detail', pk=product_id)

#     if not color_id or not size_id:
#         messages.error(request, "لطفاً رنگ و سایز محصول را انتخاب کنید.")
#         return redirect('product_detail', pk=product.id)

#     color = get_object_or_404(Color, id=color_id)
#     size = get_object_or_404(Size, id=size_id)

#     if quantity > product.inventory:
#         messages.error(request, f"موجودی کافی برای این محصول وجود ندارد. موجودی فعلی: {product.inventory}.")
#         return redirect('product_detail', pk=product.id)

#     cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)

#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product,
#         color=color,
#         size=size,
#     )

#     if not created:
#         cart_item.count += quantity
#     else:
#         cart_item.count = quantity

#     if cart_item.count > product.inventory:
#         messages.error(request, f"موجودی کافی برای این محصول وجود ندارد. موجودی فعلی: {product.inventory}.")
#         return redirect('product_detail', pk=product.id)

#     try:
#         cart_item.save()
#         product.inventory -= quantity
#         product.save()
#         messages.success(request, f"{product.title} به سبد خرید اضافه شد.")
#     except ValueError as e:
#         messages.error(request, str(e))

#     return redirect('cart_detail')

# @login_required
# def cart_detail(request):
#     cart_items = []
#     total_price = 0

#     # دریافت سبد خرید کاربر
#     cart = Cart.objects.filter(user=request.user, is_paid=False).first()

#     if cart:
#         cart_items = CartItem.objects.filter(cart=cart)
#         total_price = sum(item.product.sell_price * item.count for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }

#     return render(request, 'cart/cart_detail.html', context)


# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# # from .models import CartItem
# from cart.models import CartItem

# @login_required
# def update_cart_quantity(request, item_id):
#     cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

#     if request.method == "POST":
#         try:
#             quantity = int(json.loads(request.body).get('quantity', 1))
#         except (ValueError, TypeError):
#             return JsonResponse({'error': 'تعداد نامعتبر است.'}, status=400)

#         if quantity <= 0:
#             cart_item.delete()
#             total_cart_price = sum(
#                 item.total_price() for item in cart_item.cart.cartitem_set.all()
#             )
#             return JsonResponse({'success': True, 'deleted': True, 'total_cart_price': total_cart_price})

#         if quantity > cart_item.product.inventory:
#             return JsonResponse({'error': 'موجودی کافی نیست.'}, status=400)

#         cart_item.count = quantity
#         cart_item.save()

#         total_cart_price = sum(
#             item.total_price() for item in cart_item.cart.cartitem_set.all()
#         )

#         return JsonResponse({
#             'success': True,
#             'new_quantity': cart_item.count,
#             'new_total_price': cart_item.total_price(),
#             'total_cart_price': total_cart_price,
#         })

#     return JsonResponse({'error': 'روش درخواست معتبر نیست.'}, status=400)


# @login_required
# def remove_cart_item(request, item_id):
#     # منطق حذف آیتم از سبد خرید
#     item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
#     item.delete()
#     return redirect('cart_detail')


# def checkout_view(request):
#     # دریافت سبد خرید کاربر و سایر اطلاعات مورد نیاز
#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(cart__user=request.user, cart__is_paid=False)
#     else:
#         cart_items = []  # یا مدیریت سبد خرید برای کاربران غیراحراز هویت

#     total_price = sum(item.product.sell_price * item.count for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }
#     return render(request, 'checkout/checkout.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Product, Comment, Gallary, Color, Size, Category
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product, Category



from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products_list_category(request, category):
    if category == "all":
        # اگر دسته "تمام محصولات" انتخاب شده باشد، همه محصولات را نمایش بده
        products = Product.objects.filter(is_available=True)
        category_obj = None  
    else:
        # پیدا کردن دسته موردنظر
        category_obj = get_object_or_404(Category, en_title=category)

        # دریافت تمام زیرمجموعه‌های این دسته
        subcategories = category_obj.subcategories.all()

        # فیلتر کردن محصولات دسته موردنظر و تمام زیرمجموعه‌های آن
        products = Product.objects.filter(categories__in=[category_obj] + list(subcategories), is_available=True).distinct()

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'current_category': category_obj
    }

    return render(request, 'products/products.html', context)




from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Size, Color, Brand

def product_list_view(request, category_slug=None):
    # دریافت دسته‌بندی‌های اصلی (بدون والد)
    categories = Category.objects.filter(parent__isnull=True)
    

    # پیش‌فرض: تمامی محصولات موجود
    products = Product.objects.filter(is_available=True).distinct()
    selected_category = None
    search_query = None
    is_sale = request.GET.get('is_sale') 
    
    # اگر دسته‌بندی خاصی انتخاب شده باشد
    if category_slug:
        selected_category = get_object_or_404(Category, en_title=category_slug)
        products = products.filter(categories=selected_category)
    
    # فیلتر جستجو
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)
    
    # فیلتر تخفیف
    if is_sale == 'true':
        products = products.filter(is_sale=True)
    
    # فیلتر بر اساس سایز
    size_ids = request.GET.getlist('size')
    if size_ids:
        products = products.filter(size__id__in=size_ids).distinct()
    
    # فیلتر بر اساس رنگ
    color_ids = request.GET.getlist('color')
    if color_ids:
        products = products.filter(colors__id__in=color_ids).distinct()
    
    # فیلتر بر اساس برند
    brand_id = request.GET.get('brand')
    if brand_id:
        products = products.filter(brand__id=brand_id)

    # دریافت تمام سایزها، رنگ‌ها و برندها برای نمایش در فیلتر
    sizes = Size.objects.all().order_by('title')
    colors = Color.objects.all().order_by('title')
    brands = Brand.objects.all().order_by('title')

    # تبدیل به int با مدیریت خطا
    selected_sizes_list = []
    for sid in size_ids:
        try:
            selected_sizes_list.append(int(sid))
        except (ValueError, TypeError):
            pass
    
    selected_colors_list = []
    for cid in color_ids:
        try:
            selected_colors_list.append(int(cid))
        except (ValueError, TypeError):
            pass
    
    selected_brand_int = None
    if brand_id:
        try:
            selected_brand_int = int(brand_id)
        except (ValueError, TypeError):
            pass

    context = {
        "categories": categories,
        "selected_category": selected_category,
        "products": products,  
        "search_query": search_query,
        "sizes": sizes,
        "colors": colors,
        "brands": brands,
        "selected_sizes": selected_sizes_list,
        "selected_colors": selected_colors_list,
        "selected_brand": selected_brand_int,
    }

    
 
    
    return render(request, 'products/products.html', context)

   
   

# def product_detail_view(request, pk):
    
#     product = get_object_or_404(Product, id=pk)
#     comments = Comment.objects.filter(product=product)
#     gallery = Gallary.objects.filter(product=product)
#     categories = Category.objects.all()
#     colors = product.colors.all()
#     sizes = product.size.all()

#     context = {
#         "product": product,
#         "comments": comments,
#         "gallery": gallery,
#         "colors": colors,
#         "sizes": sizes,
#         "categories": categories,

#     }

#     return render(request, 'products/product-detail.html', context)

# # افزودن محصول به سبد خرید
# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     # بررسی موجودی محصول
#     if product.inventory is None or product.inventory <= 0:
#         messages.error(request, "این محصول در انبار موجود نیست.")
#         return redirect('product_detail', pk=product.id)

#     color_id = request.POST.get('color')
#     size_id = request.POST.get('size')
#     quantity = request.POST.get('quantity', 1)

#     try:
#         quantity = int(quantity)
#     except ValueError:
#         messages.error(request, "تعداد وارد شده نامعتبر است.")
#         return redirect('product_detail', pk=product_id)

#     if not color_id or not size_id:
#         messages.error(request, "لطفاً رنگ و سایز محصول را انتخاب کنید.")
#         return redirect('product_detail', pk=product.id)

#     color = get_object_or_404(Color, id=color_id)
#     size = get_object_or_404(Size, id=size_id)

#     if quantity > product.inventory:
#         messages.error(request, f"موجودی کافی برای این محصول وجود ندارد. موجودی فعلی: {product.inventory}.")
#         return redirect('product_detail', pk=product.id)

#     cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)

#     cart_item, created = CartItem.objects.get_or_create(
#         cart=cart,
#         product=product,
#         color=color,
#         size=size,
#     )

#     if not created:
#         cart_item.count += quantity
#     else:
#         cart_item.count = quantity

#     if cart_item.count > product.inventory:
#         messages.error(request, f"موجودی کافی برای این محصول وجود ندارد. موجودی فعلی: {product.inventory}.")
#         return redirect('product_detail', pk=product.id)

#     try:
#         cart_item.save()
#         product.inventory -= quantity
#         product.save()
#         messages.success(request, f"{product.title} به سبد خرید اضافه شد.")
#     except ValueError as e:
#         messages.error(request, str(e))

#     return redirect('cart_detail')

# # نمایش سبد خرید
# @login_required
# def cart_detail(request):
#     cart_items = []
#     total_price = 0

#     # دریافت سبد خرید کاربر
#     cart = Cart.objects.filter(user=request.user, is_paid=False).first()

#     if cart:
#         cart_items = CartItem.objects.filter(cart=cart)
#         total_price = sum(item.product.sell_price * item.count for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }

#     return render(request, 'cart/cart_detail.html', context)

# # آپدیت تعداد آیتم سبد خرید
# @login_required
# def update_cart_quantity(request, item_id):
#     cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

#     if request.method == "POST":
#         try:
#             quantity = int(json.loads(request.body).get('quantity', 1))
#         except (ValueError, TypeError):
#             return JsonResponse({'error': 'تعداد نامعتبر است.'}, status=400)

#         if quantity <= 0:
#             cart_item.delete()
#             total_cart_price = sum(
#                 item.total_price() for item in cart_item.cart.cartitem_set.all()
#             )
#             return JsonResponse({'success': True, 'deleted': True, 'total_cart_price': total_cart_price})

#         if quantity > cart_item.product.inventory:
#             return JsonResponse({'error': 'موجودی کافی نیست.'}, status=400)

#         cart_item.count = quantity
#         cart_item.save()

#         total_cart_price = sum(
#             item.total_price() for item in cart_item.cart.cartitem_set.all()
#         )

#         return JsonResponse({
#             'success': True,
#             'new_quantity': cart_item.count,
#             'new_total_price': cart_item.total_price(),
#             'total_cart_price': total_cart_price,
#         })

#     return JsonResponse({'error': 'روش درخواست معتبر نیست.'}, status=400)

# # حذف آیتم از سبد خرید
# @login_required
# def remove_cart_item(request, item_id):
#     item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
#     item.delete()
#     return redirect('cart_detail')

# # صفحه تسویه حساب
# def checkout_view(request):
#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(cart__user=request.user, cart__is_paid=False)
#     else:
#         cart_items = []  # برای کاربران غیراحتصاصی

#     total_price = sum(item.product.sell_price * item.count for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }
#     return render(request, 'checkout/checkout.html', context)


def contactus_view(request):
   return render(request, 'products/contact_us.html')

def aboutus_view(request):
    return render(request, 'products/about_us.html')

def  account_view(request):
    return render (request, 'products/account.html')




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Color, Size, Gallary
from cart.models import Cart, CartItem

def product_detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    gallery = Gallary.objects.filter(product=product)
    colors = product.colors.all()
    sizes = product.size.all()
    categories = product.categories.all()

    context = {
        "product": product,
        "gallery": gallery,
        "colors": colors,
        "sizes": sizes,
        "categories": categories,
        "first_color": colors.first() if colors.exists() else None,
        "error_message": None,
    }

    # فقط وقتی دکمه افزودن زده شده
    if request.method == "POST":
        color_id = request.POST.get("color")
        size_id = request.POST.get("size")
        count = int(request.POST.get("count", 1))

        # بررسی ورودی‌ها
        if not color_id:
            context["error_message"] = "لطفاً رنگ را انتخاب کنید."
        elif not size_id:
            context["error_message"] = "لطفاً سایز را انتخاب کنید."
        elif count < 1:
            context["error_message"] = "تعداد معتبر نیست."
        else:
            color = get_object_or_404(Color, id=color_id)
            size = get_object_or_404(Size, id=size_id)

            # --- اگر کاربر لاگین کرده ---
            if request.user.is_authenticated:
                cart, _ = Cart.objects.get_or_create(user=request.user)
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    color=color,
                    size=size,
                    defaults={'count': count}
                )
                if not created:
                    cart_item.count += count
                    cart_item.save()

            # --- اگر کاربر لاگین نکرده (session cart) ---
            else:
                session_cart = request.session.get("cart_items", [])
                merged = False
                for item in session_cart:
                    if (item["product_id"] == product.id and
                        item["color_id"] == color.id and
                        item["size_id"] == size.id):
                        item["count"] += count
                        merged = True
                        break
                if not merged:
                    session_cart.append({
                        "product_id": product.id,
                        "color_id": color.id,
                        "size_id": size.id,
                        "count": count
                    })
                request.session["cart_items"] = session_cart
                request.session.modified = True

            # ✅ موجودی کم نشه
            # product.inventory -= count  # ❌ حذف شد

            # رفتن به صفحه‌ی تأیید
            return redirect("added_to_cart", product_id=product.id)

    return render(request, "products/product-detail.html", context)
