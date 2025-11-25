from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para API REST (solo endpoints API)
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='api-category')
router.register(r'products', views.ProductViewSet, basename='api-product')
router.register(r'product-images', views.ProductImageViewSet, basename='api-productimage')

app_name = 'products'

urlpatterns = [
    # Solo incluir las rutas de API, SIN las vistas HTML
    path('', include(router.urls)),
]