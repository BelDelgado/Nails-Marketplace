from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, ProductImage, ProductView
from .serializers import (
    CategorySerializer, ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer
)
from .filters import ProductFilter


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para categorías (solo lectura)
    
    Endpoints:
    - GET /api/v1/categories/ - Listar todas las categorías
    - GET /api/v1/categories/{id}/ - Detalle de una categoría
    - GET /api/v1/categories/{id}/products/ - Productos de una categoría
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Listar productos de una categoría específica"""
        category = self.get_object()
        products = Product.objects.filter(
            category=category,
            status='available'
        ).order_by('-created_at')
        
        # Aplicar filtros
        filterset = ProductFilter(request.GET, queryset=products)
        products = filterset.qs
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)




class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para productos
    
    Endpoints:
    - GET /api/v1/products/ - Listar productos
    - POST /api/v1/products/ - Crear producto (requiere autenticación)
    - GET /api/v1/products/{id}/ - Detalle de producto
    - PUT/PATCH /api/v1/products/{id}/ - Actualizar producto (solo propietario)
    - DELETE /api/v1/products/{id}/ - Eliminar producto (solo propietario)
    
    Acciones personalizadas:
    - GET /api/v1/products/{id}/similar/ - Productos similares
    - GET /api/v1/products/my_products/ - Mis productos

    """
    queryset = Product.objects.select_related('seller', 'category').prefetch_related('images')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['created_at', 'price', 'views']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'list':
            return ProductListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer
    
    def get_queryset(self):
        """Filtrar productos según el contexto"""
        queryset = super().get_queryset()
        
        # Filtrar solo disponibles para usuarios no autenticados
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='available')
        
        return queryset
    
    def retrieve(self, request, *args, **kwargs):
        """Registrar visualización al ver detalle"""
        instance = self.get_object()
        
        # Registrar visualización
        if request.user != instance.seller:
            ProductView.objects.create(
                product=instance,
                user=request.user if request.user.is_authenticated else None,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            instance.increment_views()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        """Crear producto asignando al usuario actual"""
        serializer.save(seller=self.request.user)
    
    def perform_update(self, serializer):
        """Verificar que solo el propietario pueda actualizar"""
        if serializer.instance.seller != self.request.user:
            raise PermissionError("No tienes permiso para editar este producto")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Marcar como inactivo en lugar de eliminar"""
        if instance.seller != self.request.user:
            raise PermissionError("No tienes permiso para eliminar este producto")
        instance.status = 'inactive'
        instance.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_products(self, request):
        """Listar productos del usuario actual"""
        products = self.get_queryset().filter(seller=request.user)
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """Obtener productos similares"""
        product = self.get_object()
        
        # Buscar productos similares por categoría y precio similar
        similar_products = Product.objects.filter(
            category=product.category,
            status='available'
        ).exclude(
            id=product.id
        ).filter(
            price__gte=product.price * 0.7,  # ±30% del precio
            price__lte=product.price * 1.3
        )[:6]
        
        serializer = ProductListSerializer(
            similar_products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Productos destacados (más vistos)"""
        featured = Product.objects.filter(
            status='available'
        ).order_by('-views')[:10]
        
        serializer = ProductListSerializer(
            featured,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar imágenes de productos
    
    Endpoints:
    - GET /api/v1/product-images/ - Listar imágenes
    - POST /api/v1/product-images/ - Subir imagen
    - DELETE /api/v1/product-images/{id}/ - Eliminar imagen
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar solo imágenes de productos del usuario"""
        if self.request.user.is_authenticated:
            return self.queryset.filter(product__seller=self.request.user)
        return self.queryset.none()
    
    def perform_create(self, serializer):
        """Verificar que el producto sea del usuario"""
        product = serializer.validated_data['product']
        if product.seller != self.request.user:
            raise PermissionError("No puedes agregar imágenes a productos de otros usuarios")
        serializer.save() 
