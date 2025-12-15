from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.products.models import Product
from .models import Cart, CartItem


def cart_detail(request):
    """Vista principal del carrito"""
    return render(request, 'cart/index.html')


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Agregar producto al carrito (API)"""
    try:
        product = get_object_or_404(Product, id=product_id, active=True)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'error': 'Cantidad inválida'}, status=400)
        
        # Obtener o crear carrito
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Obtener o crear item
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.title} agregado al carrito',
            'cart_count': cart.total_items,
            'item': {
                'id': cart_item.id,
                'product_id': product.id,
                'quantity': cart_item.quantity,
                'total_price': float(cart_item.total_price)
            }
        })
        
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Actualizar cantidad de un item"""
    try:
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            cart_item.delete()
            message = 'Producto eliminado del carrito'
        else:
            cart_item.quantity = quantity
            cart_item.save()
            message = 'Cantidad actualizada'
        
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_count': cart_item.cart.total_items,
            'subtotal': float(cart_item.cart.subtotal),
            'iva': float(cart_item.cart.iva),
            'total': float(cart_item.cart.total)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Eliminar item del carrito"""
    try:
        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'cart_count': cart.total_items,
            'subtotal': float(cart.subtotal),
            'iva': float(cart.iva),
            'total': float(cart.total)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_cart_data(request):
    """Obtener datos del carrito (API)"""
    try:
        cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        
        items = [{
            'id': item.id,
            'product': {
                'id': item.product.id,
                'title': item.product.title,
                'price': float(item.product.price),
                'primary_image': item.product.primary_image.url if item.product.primary_image else None,
                'category': {
                    'name': item.product.category.name
                }
            },
            'quantity': item.quantity,
            'total_price': float(item.total_price)
        } for item in cart.items.all()]
        
        return JsonResponse({
            'items': items,
            'subtotal': float(cart.subtotal),
            'iva': float(cart.iva),
            'total': float(cart.total),
            'total_items': cart.total_items
        })
        
    except Cart.DoesNotExist:
        return JsonResponse({
            'items': [],
            'subtotal': 0,
            'iva': 0,
            'total': 0,
            'total_items': 0
        })


@login_required
def clear_cart(request):
    """Vaciar el carrito completamente"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Carrito vaciado'
        })
    except Cart.DoesNotExist:
        return JsonResponse({
            'success': True,
            'message': 'El carrito ya estaba vacío'
        })