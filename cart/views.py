from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product, Color, Size
from django.db.models import F
from django.views.decorators.http import require_POST


# ===========================
# helper: merge session cart into user cart
# ===========================
def merge_session_cart_to_user_cart(request, cart):
    session_cart = request.session.get("cart_items", [])
    for item in session_cart:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=item["product_id"],
            color_id=item.get("color_id"),
            size_id=item.get("size_id"),
            defaults={"count": item["count"], "price": item.get("price", 0)}
        )
        if not created:
            # به جای جمع کردن دستی از F() برای race condition امن استفاده می‌کنیم
            CartItem.objects.filter(pk=cart_item.pk).update(count=F("count") + item["count"])
    if session_cart:
        del request.session["cart_items"]
        request.session.modified = True


# ===========================
# افزودن محصول به سبد خرید
# ===========================
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    color_id = int(request.POST.get("color")) if request.POST.get("color") else None
    size_id = int(request.POST.get("size")) if request.POST.get("size") else None
    count = max(1, int(request.POST.get("count", 1)))

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        merge_session_cart_to_user_cart(request, cart)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            color_id=color_id,
            size_id=size_id,
            defaults={"count": count, "price": product.sell_price}
        )
        if not created:
            CartItem.objects.filter(pk=cart_item.pk).update(count=F("count") + count)

    else:
        # کاربر مهمان
        if not request.session.session_key:
            request.session.create()
        session_cart = request.session.get("cart_items", [])
        merged = False
        for item in session_cart:
            if item["product_id"] == product.id and item.get("color_id") == color_id and item.get("size_id") == size_id:
                item["count"] += count
                merged = True
                break
        if not merged:
            session_cart.append({
                "product_id": product.id,
                "color_id": color_id,
                "size_id": size_id,
                "count": count,
                "price": product.sell_price
            })
        request.session["cart_items"] = session_cart
        request.session.modified = True

    messages.success(request, f"✅ {product.title} به سبد خرید اضافه شد.")
    return redirect("added_to_cart", product_id=product.id)


# ===========================
# مشاهده سبد خرید
# ===========================
def cart_detail(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        merge_session_cart_to_user_cart(request, cart)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)

    cart_items = CartItem.objects.filter(cart=cart).select_related("product", "color", "size")

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("count_"):
                item_id = key.split("_")[1]
                item = get_object_or_404(CartItem, id=item_id, cart=cart)
                new_count = int(value)
                if new_count <= 0:
                    item.delete()
                else:
                    item.count = new_count
                    item.save()
            elif key.startswith("delete_"):
                item_id = key.split("_")[1]
                CartItem.objects.filter(id=item_id, cart=cart).delete()

    total_price = sum(item.subtotal for item in cart_items)

    return render(request, "cart/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
    })


# ===========================
# تسویه حساب
# ===========================
def checkout_view(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        merge_session_cart_to_user_cart(request, cart)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)

    cart_items = CartItem.objects.filter(cart=cart).select_related("product", "color", "size")

    if request.method == "POST":
        if not cart_items.exists():
            messages.warning(request, "سبد خرید شما خالی است.")
            return redirect("cart_detail")

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal_code")

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            address=address,
            postal_code=postal_code,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                color=item.color,
                size=item.size,
                quantity=item.count,
                price=item.price,
            )

        cart_items.delete()
        if request.user.is_authenticated:
            cart.delete()

        messages.success(request, "✅ سفارش شما ثبت شد.")
        return redirect("order_success")

    # GET request → نمایش صفحه checkout
    return render(request, "cart/checkout.html", {"cart": cart, "cart_items": cart_items})


# ===========================
# صفحه موفقیت سفارش
# ===========================
def order_success(request):
    return render(request, "cart/order_success.html")


# ===========================
# صفحه اضافه شدن محصول به سبد
# ===========================
def added_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "cart/added_to_cart.html", {"product": product})
