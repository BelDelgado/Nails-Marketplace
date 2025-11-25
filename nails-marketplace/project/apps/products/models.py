from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User

class Category(models.Model):
    """
    Categorías de productos para insumos de uñas
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icono (nombre)')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Imagen')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    """
    Productos de insumos para uñas
    """
    TYPE_CHOICES = [
        ('sale', 'Venta'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'Nuevo'),
        ('like_new', 'Como nuevo'),
        ('good', 'Buen estado'),
        ('fair', 'Estado aceptable'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('reserved', 'Reservado'),
        ('sold', 'Vendido'),
        ('inactive', 'Inactivo'),
    ]
    
    # Información básica
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name='Vendedor')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Categoría')
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    
    # Tipo y condición
    product_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='sale', verbose_name='Tipo')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='new', verbose_name='Condición')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available', verbose_name='Estado')
    
    # Precio y stock
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name='Precio'
    )
    stock = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Stock disponible'
    )
    
    # Marca y detalles específicos
    brand = models.CharField(max_length=100, blank=True, verbose_name='Marca')
    color = models.CharField(max_length=50, blank=True, verbose_name='Color')
    size = models.CharField(max_length=50, blank=True, verbose_name='Tamaño/Volumen')
    
    # Ubicación (heredada del vendedor o específica)
    city = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    state = models.CharField(max_length=100, blank=True, verbose_name='Provincia')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Métricas
    views = models.IntegerField(default=0, verbose_name='Visualizaciones')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de vencimiento')
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['seller', 'status']),
        ]
    
    def __str__(self):
        return f"{self.title} - ${self.price}"
    
    def is_available(self):
        """Verificar si el producto está disponible"""
        return self.status == 'available' and self.stock > 0
    
    def increment_views(self):
        """Incrementar contador de vistas"""
        self.views += 1
        self.save(update_fields=['views'])

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_subtotal(self):
        return self.product.price * self.quantity

class ProductImage(models.Model):
    """
    Imágenes de productos
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Producto')
    image = models.ImageField(upload_to='products/%Y/%m/', verbose_name='Imagen')
    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Texto alternativo')
    is_primary = models.BooleanField(default=False, verbose_name='Imagen principal')
    order = models.IntegerField(default=0, verbose_name='Orden')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imágenes de Productos'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Imagen de {self.product.title}"
    
    def save(self, *args, **kwargs):
        """Si es imagen principal, quitar flag de otras imágenes"""
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class ProductView(models.Model):
    """
    Registro de visualizaciones de productos (para analytics)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='view_logs', verbose_name='Producto')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuario')
    ip_address = models.GenericIPAddressField(verbose_name='Dirección IP')
    user_agent = models.TextField(blank=True, verbose_name='User Agent')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de visualización')
    
    class Meta:
        verbose_name = 'Visualización'
        verbose_name_plural = 'Visualizaciones'
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.product.title} - {self.viewed_at}"
 