from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "color", "size", "quantity", "price", "total_price")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at", "is_checked")
    inlines = [OrderItemInline]

admin.site.register(Cart)
admin.site.register(CartItem)