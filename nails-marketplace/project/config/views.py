from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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


