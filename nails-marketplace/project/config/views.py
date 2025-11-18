from django.shortcuts import render
from apps.users.models import User
from apps.products.models import Product


def home_view(request):
    """Vista para la página de inicio"""
    
    # Obtener estadísticas
    total_users = User.objects.count()
    total_products = Product.objects.filter(status='available').count()
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
    }
    
    return render(request, 'home/index.html', context)