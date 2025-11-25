from django.contrib import admin
from .models import Category, Product, ProductImage, ProductView, Cart, CartItem


class ProductImageInline(admin.TabularInline):
    """Inline para imágenes de productos"""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Administración de categorías"""
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Administración de productos"""
    list_display = [
        'title', 'seller', 'category', 'price', 'stock', 
        'product_type', 'condition', 'status', 'views', 'created_at'
    ]
    list_filter = [
        'status', 'product_type', 'condition', 'category', 
        'created_at', 'updated_at'
    ]
    search_fields = ['title', 'description', 'seller__username', 'brand']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('seller', 'category', 'title', 'description')
        }),
        ('Tipo y Estado', {
            'fields': ('product_type', 'condition', 'status')
        }),
        ('Precio y Stock', {
            'fields': ('price', 'stock')
        }),
        ('Detalles del Producto', {
            'fields': ('brand', 'color', 'size'),
            'classes': ('collapse',)
        }),
        ('Ubicación', {
            'fields': ('city', 'state', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
    
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_available', 'mark_as_sold', 'mark_as_inactive']
    
    def mark_as_available(self, request, queryset):
        """Marcar productos como disponibles"""
        updated = queryset.update(status='available')
        self.message_user(request, f'{updated} productos marcados como disponibles.')
    mark_as_available.short_description = 'Marcar como disponibles'
    
    def mark_as_sold(self, request, queryset):
        """Marcar productos como vendidos"""
        updated = queryset.update(status='sold')
        self.message_user(request, f'{updated} productos marcados como vendidos.')
    mark_as_sold.short_description = 'Marcar como vendidos'
    
    def mark_as_inactive(self, request, queryset):
        """Marcar productos como inactivos"""
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} productos marcados como inactivos.')
    mark_as_inactive.short_description = 'Marcar como inactivos'


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    """Administración de visualizaciones"""
    list_display = ['product', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product__title', 'user__username', 'ip_address']
    readonly_fields = ['viewed_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Administración de carritos"""
    list_display = ['user', 'created_at', 'updated_at', 'get_items_count', 'get_total']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = ['user__username']
    
    def get_items_count(self, obj):
        return obj.items.count()
    get_items_count.short_description = 'Cantidad de items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Administración de items del carrito"""
    list_display = ['cart', 'product', 'quantity', 'get_subtotal', 'added_at']
    readonly_fields = ['added_at']
    search_fields = ['cart__user__username', 'product__title']