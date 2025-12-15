import django_filters
from django.db import models
from .models import Product, Category  # ← Agregar Category aquí


class ProductFilter(django_filters.FilterSet):
    """
    Filtros para productos de insumos de uñas
    """
    # Filtros de precio
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Búsqueda por título, descripción o marca
    search = django_filters.CharFilter(method='filter_search')
    
    # Filtro por ubicación
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter(lookup_expr='icontains')
    
    # Filtros por tipo y condición
    product_type = django_filters.MultipleChoiceFilter(choices=Product.TYPE_CHOICES)
    condition = django_filters.MultipleChoiceFilter(choices=Product.CONDITION_CHOICES)
    status = django_filters.MultipleChoiceFilter(choices=Product.STATUS_CHOICES)
    
    # Filtro por categoría
    category = django_filters.NumberFilter(field_name='category__id')
    category_slug = django_filters.CharFilter(field_name='category__slug')
    
    # Filtro por vendedor
    seller = django_filters.NumberFilter(field_name='seller__id')
    seller_username = django_filters.CharFilter(field_name='seller__username', lookup_expr='iexact')
    
    # Filtros por marca y color
    brand = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='icontains')
    
    # Ordenamiento
    ordering = django_filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('price', 'price'),
            ('views', 'views'),
            ('title', 'title'),  # ← Agregué este para ordenar por nombre
        ),
        field_labels={
            'created_at': 'Fecha de publicación',
            'price': 'Precio',
            'views': 'Visualizaciones',
            'title': 'Nombre',
        }
    )
    
    class Meta:
        model = Product
        fields = []
    
    def filter_search(self, queryset, name, value):
        """
        Búsqueda en múltiples campos
        """
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(brand__icontains=value)
        )