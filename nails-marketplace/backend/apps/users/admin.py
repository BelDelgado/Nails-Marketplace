from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Reputation, Review


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Administración personalizada de usuarios"""
    list_display = ['username', 'email', 'role', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('phone', 'role', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'phone', 'role')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Administración de perfiles"""
    list_display = ['user', 'city', 'state', 'country', 'created_at']
    list_filter = ['country', 'state']
    search_fields = ['user__username', 'user__email', 'city', 'address']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Reputation)
class ReputationAdmin(admin.ModelAdmin):
    """Administración de reputaciones"""
    list_display = ['user', 'average_rating', 'total_sales', 'total_purchases', 'is_verified_seller', 'is_top_seller']
    list_filter = ['is_verified_seller', 'is_top_seller']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Estadísticas', {
            'fields': ('total_sales', 'total_purchases')
        }),
        ('Calificaciones', {
            'fields': ('positive_reviews', 'negative_reviews', 'average_rating')
        }),
        ('Badges', {
            'fields': ('is_verified_seller', 'is_top_seller')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Administración de reseñas"""
    list_display = ['reviewer', 'reviewed', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['reviewer__username', 'reviewed__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuarios', {
            'fields': ('reviewer', 'reviewed')
        }),
        ('Calificación', {
            'fields': ('rating', 'comment')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )