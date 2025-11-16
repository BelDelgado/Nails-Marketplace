from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Vista de inicio simple
def api_root(request):
    return JsonResponse({
        'message': 'Bienvenido a Nails Marketplace API',
        'version': 'v1',
        'endpoints': {
            'documentation': '/swagger/',
            'admin': '/admin/',
            'api': '/api/v1/',
        }
    })

# Configuración de Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Nails Marketplace API",
        default_version='v1',
        description="API REST para marketplace de insumos de uñas",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contacto@nailsmarketplace.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation (Swagger)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API v1
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.products.urls')),
    
    # Futuras apps
    # path('api/v1/', include('apps.chat.urls')),
    # path('api/v1/', include('apps.payments.urls')),
    # path('api/v1/', include('apps.locations.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
# Personalizar el admin
admin.site.site_header = "Nails Marketplace Admin"
admin.site.site_title = "Nails Marketplace"
admin.site.index_title = "Panel de Administración"