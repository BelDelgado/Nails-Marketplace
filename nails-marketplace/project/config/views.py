from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import User
from apps.products.models import Product
from apps.products.models import Category

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

@login_required
def profile_dashboard(request):
    return render(request, 'profile/dashboard.html')

@login_required
def profile_edit(request):
    """Editar perfil del usuario"""
    if request.method == 'POST':
        user = request.user
        profile = user.profile
        
        # Actualizar datos del usuario
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone', '')
        user.save()
        
        # Actualizar perfil
        profile.bio = request.POST.get('bio', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.address = request.POST.get('address', '')
        profile.instagram = request.POST.get('instagram', '')
        profile.facebook = request.POST.get('facebook', '')
        profile.whatsapp = request.POST.get('whatsapp', '')
        
        # Actualizar avatar si se subió uno
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        messages.success(request, '¡Perfil actualizado exitosamente!')
        return redirect('profile_dashboard')
    
    return render(request, 'profile/edit.html') 

# Productos
def categories_view(request):
    """Vista para mostrar todas las categorías"""
    categories = Category.objects.filter(is_active=True).prefetch_related('products')
    return render(request, 'products/categories.html', {
        'categories': categories
    })

def products_list_view(request):
    """Vista de listado de productos"""
    return render(request, 'products/list.html')


def product_detail_view(request, pk):
    """Vista de detalle de producto"""
    return render(request, 'products/detail.html', {'product_id': pk})


@login_required
def product_create_view(request):
    """Vista para crear producto"""
    return render(request, 'products/create.html')


# Carrito
def cart_view(request):
    """Vista del carrito de compras"""
    return render(request, 'cart/index.html')
