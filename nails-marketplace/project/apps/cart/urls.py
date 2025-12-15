from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Vista principal del carrito
    path('', views.cart_detail, name='cart_detail'),
    
    # API endpoints
    path('api/data/', views.get_cart_data, name='get_cart_data'),
    path('api/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('api/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('api/clear/', views.clear_cart, name='clear_cart'),
]