from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # صفحه اصلی محصولات
    path('', products_list_view, name='product_list'),

    # جزئیات محصول
    path('product-detail/<int:pk>/', product_detail_view, name='product_detail'),

    # دسته‌بندی و زیر دسته‌بندی داینامیک
    path('category/<str:category_slug>/', products_list_view, name='products_by_category'),

    # سبد خرید
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart-quantity/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('cart/', cart_detail, name='cart_detail'),
    path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
    path('checkout/', checkout_view, name='checkout'),

    # صفحات اطلاعاتی
    path('contact/', contactus_view, name='contactus'),
    path('aboutus/', aboutus_view, name='aboutus'),
    path('account/', account_view, name='account'),

    # بازیابی رمز عبور
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
