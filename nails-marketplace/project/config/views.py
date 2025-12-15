from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.products.models import Category, Product, ProductView
from apps.products.forms import ProductForm, ProductImage 
from apps.cart.models import Cart, CartItem 
from django.db.models import Q, Count


def home_view(request):
    """Vista principal del home"""
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Contar usuarios y productos
    total_users = User.objects.count()
    total_products = Product.objects.filter(status='available').count()
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
    }
    
    return render(request, 'home/index.html', context)
    
def products_list_view(request):
    """Vista de listado de productos con filtros"""
    # Obtener todos los productos disponibles
    products = Product.objects.filter(
        status='available'
    ).select_related('seller', 'category').prefetch_related('images')
    
    # Filtrar por categoría si viene en la URL
    category_slug = request.GET.get('category')
    selected_category = None
    
    if category_slug:
        try:
            selected_category = Category.objects.get(slug=category_slug, is_active=True)
            products = products.filter(category=selected_category)
        except Category.DoesNotExist:
            pass
    
    # Filtrar por búsqueda
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Ordenar productos
    order_by = request.GET.get('order', '-created_at')
    valid_orders = ['-created_at', 'price', '-price', 'title']
    if order_by in valid_orders:
        products = products.order_by(order_by)
    
    # Obtener todas las categorías para el filtro
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__status='available'))
    )
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'total_products': products.count(),
    }
    
    return render(request, 'products/list.html', context)

# VISTAS DE PERFIL
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

# VISTAS DE PRODUCTOS

def categories_view(request):
    """Vista para mostrar todas las categorías"""
    categories = Category.objects.filter(is_active=True).prefetch_related('products')
    return render(request, 'products/categories.html', {
        'categories': categories
    })

def category_detail_view(request, slug):
    """Vista de detalle de una categoría con sus productos"""
    # Obtener la categoría
    category = get_object_or_404(Category, slug=slug, is_active=True)
    # Obtener productos de esta categoría
    products = Product.objects.filter(
        category=category,
        status='available'
    ).select_related('seller', 'category').prefetch_related('images')
    
    # Filtrar por búsqueda dentro de la categoría
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Ordenar productos
    order_by = request.GET.get('order', '-created_at')
    valid_orders = ['-created_at', 'price', '-price', 'title']
    if order_by in valid_orders:
        products = products.order_by(order_by)
    
    # Otras categorías para mostrar en sidebar
    other_categories = Category.objects.filter(
        is_active=True
    ).exclude(id=category.id).annotate(
        product_count=Count('products', filter=Q(products__status='available'))
    )[:5]
    
    context = {
        'category': category,
        'products': products,
        'other_categories': other_categories,
        'search_query': search_query,
        'total_products': products.count(),
    }
    
    return render(request, 'products/category_detail.html', context)

def products_list_view(request):
    """Vista de listado de productos"""
    # Inicializar queryset
    products = Product.objects.filter(
        status='available'
    ).select_related('seller', 'category').prefetch_related('images')
    
    # Filtrar por búsqueda si existe
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Obtener categorías
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    
    return render(request, 'products/list.html', context)

def product_detail_view(request, pk):
    """Vista de detalle de producto"""
    # Obtener el producto con todas sus relaciones
    product = get_object_or_404(
        Product.objects.select_related('seller', 'category').prefetch_related('images'),
        pk=pk
    )
    
    # Incrementar vistas solo si no es el vendedor
    if not request.user.is_authenticated or request.user != product.seller:
        product.increment_views()
        
        # Registrar visualización
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        ProductView.objects.create(
            product=product,
            user=request.user if request.user.is_authenticated else None,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    
    # Productos similares
    similar_products = Product.objects.filter(
        category=product.category,
        status='available'
    ).exclude(id=product.id).select_related('category', 'seller').prefetch_related('images')[:4]
    
    return render(request, 'products/detail.html', {
        'product': product,
        'similar_products': similar_products
    })

@login_required
def product_create_view(request):
    """Vista para crear producto"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        images = request.FILES.getlist('images')
        
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.status = 'available'
            product.save()
            
            # Guardar imágenes
            for index, image in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_primary=(index == 0),
                    order=index
                )
            
            messages.success(request, '¡Producto creado exitosamente!')
            return redirect('product_detail', pk=product.id)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductForm()
    
    return render(request, 'products/create.html', {
        'form': form
    })

@login_required
def product_edit_view(request, pk):
    """Vista para editar producto"""
    # Obtener el producto
    product = get_object_or_404(
        Product.objects.select_related('seller', 'category').prefetch_related('images'),
        pk=pk
    )
    
    # Verificar que el usuario sea el dueño
    if request.user != product.seller:
        messages.error(request, 'No tienes permiso para editar este producto.')
        return redirect('product_detail', pk=pk)
    
    # Obtener categorías para el formulario
    categories = Category.objects.filter(is_active=True)
    
    return render(request, 'products/edit.html', {
        'product': product,
        'categories': categories
    })

@login_required
def product_delete_view(request, pk):
    """Vista para eliminar producto"""
    from django.contrib import messages
    
    # Obtener el producto
    product = get_object_or_404(Product, pk=pk)
    
    # Verificar que el usuario sea el dueño
    if request.user != product.seller:
        messages.error(request, 'No tienes permiso para eliminar este producto.')
        return redirect('product_detail', pk=pk)
    
    if request.method == 'POST':
        # Guardar el título para el mensaje
        product_title = product.title
        # Marcar el producto como inactivo en lugar de eliminarlo
        product.status = 'inactive'
        product.save()
        
        messages.success(request, f'El producto "{product_title}" ha sido eliminado.')
        return redirect('profile_dashboard')
    
    # Si es GET, mostrar página de confirmación
    return render(request, 'products/delete_confirm.html', {'product': product})
# ============================================
# VISTAS DEL CARRITO
# ============================================

def cart_view(request):
    """Vista del carrito"""
    if not request.user.is_authenticated:
        return render(request, 'cart/index.html', {
            'cart': None,
            'items': [],
            'total': 0
        })
    
    # Obtener o crear carrito del usuario
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product').prefetch_related('product__images')
    total = cart.get_total()
    
    return render(request, 'cart/index.html', {
        'cart': cart,
        'items': items,
        'total': total
    })


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    try:
        product = Product.objects.get(id=product_id, status='available')
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Verificar si ya existe en el carrito
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            # Si ya existe, aumentar cantidad
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Stock insuficiente'
                }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': 'Producto agregado al carrito',
            'cart_count': cart.items.count()
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Producto no encontrado'
        }, status=404)


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Eliminar item del carrito"""
    try:
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(id=item_id, cart=cart)
        item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'cart_count': cart.items.count(),
            'cart_total': float(cart.get_total())
        })
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({
            'success': False, 
            'message': 'Item no encontrado'
        }, status=404)


@login_required
@require_POST
def update_cart_quantity(request, item_id):
    """Actualizar cantidad de un item"""
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            return JsonResponse({
                'success': False, 
                'message': 'Cantidad inválida'
            }, status=400)
        
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(id=item_id, cart=cart)
        
        if quantity > item.product.stock:
            return JsonResponse({
                'success': False, 
                'message': 'Stock insuficiente'
            }, status=400)
        
        item.quantity = quantity
        item.save()
        
        return JsonResponse({
            'success': True,
            'subtotal': float(item.get_subtotal()),
            'cart_total': float(cart.get_total())
        })
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({
            'success': False, 
            'message': 'Item no encontrado'
        }, status=404)


# ============================================
# OTRAS VISTAS (HOME, PROFILE, ETC)
# ============================================

def home_view(request):
    """Vista de la página principal"""
    return render(request, 'home/index.html')


@login_required
def profile_dashboard(request):
    """Dashboard del perfil"""
    return render(request, 'profile/dashboard.html')


@login_required
def profile_edit(request):
    """Editar perfil"""
    return render(request, 'profile/edit.html')