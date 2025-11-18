from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    ProductImageViewSet,
    FavoriteViewSet,
    ExchangeRequestViewSet
)

app_name = 'products'

# Router para ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='product-image')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'exchange-requests', ExchangeRequestViewSet, basename='exchange-request')

urlpatterns = [
    path('', include(router.urls)),
]