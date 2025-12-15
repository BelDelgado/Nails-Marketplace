from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (home_view, 
                    profile_dashboard, 
                    profile_edit, 
                    categories_view, 
                    category_detail_view, 
                    products_list_view,
                    product_detail_view, 
                    product_create_view,  
                    product_edit_view, 
                    product_delete_view,
                    cart_view, 
                    add_to_cart,
                    remove_from_cart, 
                    update_cart_quantity)     

urlpatterns = [
    # Home
    path('', home_view, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # AllAuth URLs
    path("accounts/", include("allauth.urls")),  
    path('api-auth/', include('rest_framework.urls')),

    # Profile URLs
    path('profile/', profile_dashboard, name='profile_dashboard'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    
     # Products
    path('categories/',  categories_view, name='categories'),
    path('category/<slug:slug>/', category_detail_view, name='category_detail'),
    path('products/', products_list_view, name='products_list'),
    path('products/create/', product_create_view, name='product_create'),
    path('products/<int:pk>/delete/', product_delete_view, name='product_delete'),
    path('products/<int:pk>/', product_detail_view, name='product_detail'),
    path('products/<int:pk>/edit/', product_edit_view, name='product_edit'),
   

    # Cart
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', update_cart_quantity, name='update_cart_quantity'),
     
    # API v1
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/', include('apps.products.urls'))
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Personalizar admin
admin.site.site_header = "Nails Marketplace Admin"
admin.site.site_title = "Nails Marketplace"
admin.site.index_title = "Panel de Administración"