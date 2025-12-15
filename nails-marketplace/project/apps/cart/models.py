from django.db import models
from apps.users.models import User
from apps.products.models import Product


class Cart(models.Model):
    """Carrito de compras del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def get_total(self):
        """Calcular el total del carrito"""
        from decimal import Decimal
        total = Decimal('0.00')
        for item in self.items.all():
            total += item.get_subtotal()
        return total

    def __str__(self):
        return f"Carrito de {self.user.username}"


class CartItem(models.Model):
    """Item individual en el carrito"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
        unique_together = ('cart', 'product')  # Un producto solo una vez por carrito

    def get_subtotal(self):
        """Calcular subtotal del item"""
        from decimal import Decimal
        return Decimal(str(self.product.price)) * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.product.title}"