# # from django.urls import path
# # from .views import product_list_view, product_detail_view,  product_list_category_viewو 
# # urlpatterns = [
# #    path('', product_list_view, name ='productlis'),
# #    path('product-detail/<pk>/', product_detail_view),
# #    path('products/<category>', product_list_category_view),
   
# # from django.urls import path
# # from .views import product_list_view, product_detail_view, product_list_category_view, add_to_cart ,cart_detail, remove_cart_item ,checkout_view

# # urlpatterns = [
# #     path('', product_list_view, name='productlis'),  # نمایش لیست محصولات
# #     path('product-detail/<int:pk>/', product_detail_view, name='product_detail'),  # جزئیات محصول
# #     path('products/<str:category>/', product_list_category_view, name='product_list_category'),  # لیست محصولات بر اساس دسته‌بندی
# #     path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'), 
# #     path('cart/', cart_detail, name='cart_detail'),
# #     path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),
# #      path('checkout/', checkout_view, name='checkout'),
# # ]

# # from django.urls import path
# # from django.contrib.auth import views as auth_views
# # from .views import (
# #     product_list_view,
# #     product_detail_view,
# #     product_list_category_view,
# #     add_to_cart,
# #     cart_detail,
# #     remove_cart_item,
# #     checkout_view,
# #     update_cart_quantity,  # مسیر جدید
# # )

# # urlpatterns = [
# #     # مسیرهای مربوط به محصولات
# #     path('', product_list_view, name='productlis'),  # نمایش لیست محصولات
# #     path('product-detail/<int:pk>/', product_detail_view, name='product_detail'),  # جزئیات محصول
# #     path('products/<str:category>/', product_list_category_view, name='product_list_category'),  # محصولات براساس دسته‌بندی

# #     # مسیرهای مربوط به سبد خرید
# #     path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # افزودن محصول به سبد خرید
# #     path('update-cart-quantity/', update_cart_quantity, name='update_cart_quantity'),  # به‌روزرسانی تعداد محصول در سبد
# #     path('cart/', cart_detail, name='cart_detail'),  # نمایش جزئیات سبد خرید
# #     path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),  # حذف محصول از سبد خرید

# #     # مسیر تسویه حساب
# #     path('checkout/', checkout_view, name='checkout'),  # صفحه تسویه حساب

# #     # مسیرهای بازیابی رمز عبور
# #     path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # شروع فرایند بازیابی رمز
# #     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # تایید ارسال ایمیل
# #     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # تایید تغییر رمز
# #     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # پایان بازیابی رمز عبور
# #     # تغییر مسیر برای update-cart-quantity به همراه item_id
# #     path('update-cart-quantity/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),  # به‌روزرسانی تعداد محصول در سبد
    
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from .views import (
#     product_list_view,
#     product_detail_view,
#     product_list_category_view,
#     add_to_cart,
#     cart_detail,
#     remove_cart_item,
#     checkout_view,
#     update_cart_quantity, 
#     category_products, # ویو برای به‌روزرسانی تعداد
# )

# urlpatterns = [
#     # مسیرهای مربوط به محصولات
#     path('', product_list_view, name='productlis'),  # نمایش لیست محصولات
#     path('product-detail/<int:pk>/', product_detail_view, name='product_detail'),  # جزئیات محصول
#     path('products/<str:category>/', product_list_category_view, name='product_list_category'),  # محصولات براساس دسته‌بندی

#     # مسیرهای مربوط به سبد خرید
#     path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),  # افزودن محصول به سبد خرید
#     path('update-cart-quantity/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),  # به‌روزرسانی تعداد محصول در سبد
#     path('cart/', cart_detail, name='cart_detail'),  # نمایش جزئیات سبد خرید
#     path('remove-cart-item/<int:item_id>/', remove_cart_item, name='remove_cart_item'),  # حذف محصول از سبد خرید

#     # مسیر تسویه حساب
#     path('checkout/', checkout_view, name='checkout'),  # صفحه تسویه حساب

#     # مسیرهای بازیابی رمز عبور
#     path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # شروع فرایند بازیابی رمز
#     path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # تایید ارسال ایمیل
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # تایید تغییر رمز
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
#     path('category/<str:category_slug>/', category_products, name='category_products'), # پایان بازیابی رمز عبور
# ]

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    # مسیرهای مربوط به محصولات
    path('', product_list_view, name='productlis'),  # نمایش لیست محصولات
    path('product-detail/<int:pk>/', product_detail_view, name='product_detail'),  # جزئیات محصول
    
    # path('products/<str:category>/', product_list_category_view, name='product_list_category'),  # محصولات براساس دسته‌بندی

    # مسیرهای مربوط به سبد خرید
    

    # مسیرهای بازیابی رمز عبور
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # شروع فرایند بازیابی رمز
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # تایید ارسال ایمیل
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # تایید تغییر رمز
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
    path('contact/', contactus_view, name='contactus'),
    path('aboutus/', aboutus_view, name='aboutus'),
    path('account/', account_view, name='account'),
    path('category/<str:category>/', products_list_category, name='products_by_category'),
   
    # path('category/<str:category_slug>/', category_products, name='category_products'),

  
]