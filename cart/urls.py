from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart_detail, name="cart_detail"),
     path("cart", views.cart_detail, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("success/", views.order_success, name="order_success"),
    path("added-to-cart/<int:product_id>/", views.added_to_cart, name="added_to_cart"),
]
