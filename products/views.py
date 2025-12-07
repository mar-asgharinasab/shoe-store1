from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Comment, Gallary, Color, Size, Brand
from cart.models import Cart, CartItem

# ===========================
# لیست محصولات و دسته‌بندی‌ها
# ===========================
def products_list_view(request, category_slug=None):
    """
    نمایش محصولات با فیلترها و دسته‌بندی‌ها.
    category_slug: اسلاگ دسته یا زیرشاخه. اگر None باشد، تمام محصولات نمایش داده می‌شوند.
    """
    # دسته‌های والد برای منو
    categories = Category.objects.filter(parent__isnull=True)

    # حالت "تمام محصولات"
    if category_slug in [None, "all"]:
        products = Product.objects.filter(is_available=True).distinct()
        current_category = None
        subcategories = []
    else:
        # پیدا کردن دسته یا زیرشاخه
        current_category = get_object_or_404(Category, slug=category_slug)
        subcategories = current_category.children.all()
        products = Product.objects.filter(
            is_available=True,
            categories__in=[current_category] + list(subcategories)
        ).distinct()

    # فیلتر جستجو
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(title__icontains=search_query)

    # فیلتر تخفیف
    if request.GET.get('is_sale') == 'true':
        products = products.filter(is_sale=True)

    # فیلتر سایز، رنگ و برند
    size_ids = request.GET.getlist('size')
    if size_ids:
        products = products.filter(size__id__in=size_ids).distinct()

    color_ids = request.GET.getlist('color')
    if color_ids:
        products = products.filter(colors__id__in=color_ids).distinct()

    brand_id = request.GET.get('brand')
    if brand_id:
        products = products.filter(brand__id=brand_id)

    # اطلاعات فیلترها برای نمایش
    sizes = Size.objects.all().order_by('title')
    colors = Color.objects.all().order_by('title')
    brands = Brand.objects.all().order_by('title')

    context = {
        "products": products,
        "categories": categories,
        "current_category": current_category,
        "subcategories": subcategories,
        "sizes": sizes,
        "colors": colors,
        "brands": brands,
        "selected_sizes": [int(sid) for sid in size_ids if sid.isdigit()],
        "selected_colors": [int(cid) for cid in color_ids if cid.isdigit()],
        "selected_brand": int(brand_id) if brand_id and brand_id.isdigit() else None,
        "search_query": search_query,
    }
    return render(request, "products/products.html", context)


# ===========================
# جزئیات محصول
# ===========================
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

    if request.method == "POST":
        color_id = request.POST.get("color")
        size_id = request.POST.get("size")
        count = request.POST.get("count") or request.POST.get("quantity") or 1
        try:
            count = int(count)
        except (TypeError, ValueError):
            count = 1

        if not color_id:
            context["error_message"] = "لطفاً رنگ را انتخاب کنید."
        elif not size_id:
            context["error_message"] = "لطفاً سایز را انتخاب کنید."
        elif count < 1:
            context["error_message"] = "تعداد معتبر نیست."
        else:
            color = get_object_or_404(Color, id=color_id)
            size = get_object_or_404(Size, id=size_id)

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

            return redirect("added_to_cart", product_id=product.id)

    return render(request, "products/product-detail.html", context)


# ===========================
# صفحات اطلاعاتی
# ===========================
def contactus_view(request):
    return render(request, 'products/contact_us.html')

def aboutus_view(request):
    return render(request, 'products/about_us.html')

def account_view(request):
    return render(request, 'products/account.html')


# ===========================
# سبد خرید
# ===========================
@login_required
def add_to_cart(request, product_id):
    pass  # می‌توانی کد خودت را اینجا بذاری

@login_required
def cart_detail(request):
    pass

@login_required
def update_cart_quantity(request, item_id):
    pass

@login_required
def remove_cart_item(request, item_id):
    pass

def checkout_view(request):
    pass
