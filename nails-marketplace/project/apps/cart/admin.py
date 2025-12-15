from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline para items del carrito"""
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'get_subtotal_display']
    fields = ['product', 'quantity', 'get_subtotal_display', 'added_at']
    
    def get_subtotal_display(self, obj):
        if obj.id:
            return f"${obj.get_subtotal():.2f}"
        return "-"
    get_subtotal_display.short_description = 'Subtotal'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Administración de carritos"""
    list_display = ['user', 'get_items_count', 'get_total_display', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'get_total_display']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Cantidad de items'
    
    def get_total_display(self, obj):
        return f"${obj.get_total():.2f}"
    get_total_display.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Administración de items del carrito"""
    list_display = ['cart', 'product', 'quantity', 'get_subtotal_display', 'added_at']
    readonly_fields = ['added_at', 'get_subtotal_display']
    search_fields = ['cart__user__username', 'product__title']
    list_filter = ['added_at']
    
    def get_subtotal_display(self, obj):
        return f"${obj.get_subtotal():.2f}"
    get_subtotal_display.short_description = 'Subtotal'