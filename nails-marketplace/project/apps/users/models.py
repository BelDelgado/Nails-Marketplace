from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    """
    Usuario personalizado extendido de AbstractUser
    """
    ROLE_CHOICES = [
        ('buyer', 'Comprador'),
        ('seller', 'Vendedor'),
        ('admin', 'Administrador'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer', verbose_name='Rol')
    is_verified = models.BooleanField(default=False, verbose_name='Email verificado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Profile(models.Model):
    """
    Perfil del usuario con información adicional
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='profiles/avatars/', blank=True, null=True, verbose_name='Avatar')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biografía')
    
    # Ubicación
    address = models.CharField(max_length=255, blank=True, verbose_name='Dirección')
    city = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    state = models.CharField(max_length=100, blank=True, verbose_name='Provincia/Estado')
    country = models.CharField(max_length=100, default='Argentina', verbose_name='País')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Código Postal')
    
    # Geolocalización
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Redes sociales (para vendedores)
    instagram = models.CharField(max_length=100, blank=True, verbose_name='Instagram')
    facebook = models.CharField(max_length=100, blank=True, verbose_name='Facebook')
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name='WhatsApp')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"Perfil de {self.user.username}"


class Reputation(models.Model):
    """
    Sistema de reputación para vendedores y compradores
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reputation')
    
    # Estadísticas
    total_sales = models.IntegerField(default=0, verbose_name='Ventas totales')
    total_purchases = models.IntegerField(default=0, verbose_name='Compras totales')
    
    # Calificaciones
    positive_reviews = models.IntegerField(default=0, verbose_name='Reseñas positivas')
    negative_reviews = models.IntegerField(default=0, verbose_name='Reseñas negativas')
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Calificación promedio'
    )
    
    # Badges/Insignias
    is_verified_seller = models.BooleanField(default=False, verbose_name='Vendedor verificado')
    is_top_seller = models.BooleanField(default=False, verbose_name='Vendedor destacado')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reputación'
        verbose_name_plural = 'Reputaciones'
    
    def __str__(self):
        return f"Reputación de {self.user.username} - {self.average_rating}★"
    
    def calculate_average_rating(self):
        """Calcular calificación promedio"""
        total_reviews = self.positive_reviews + self.negative_reviews
        if total_reviews == 0:
            return 0.00
        
        # Asumiendo positivas = 5★ y negativas = 1★
        total_points = (self.positive_reviews * 5) + (self.negative_reviews * 1)
        self.average_rating = round(total_points / total_reviews, 2)
        self.save()
        return self.average_rating


class Review(models.Model):
    """
    Reseñas entre usuarios (comprador → vendedor o viceversa)
    """
    RATING_CHOICES = [
        (1, '⭐ Muy malo'),
        (2, '⭐⭐ Malo'),
        (3, '⭐⭐⭐ Regular'),
        (4, '⭐⭐⭐⭐ Bueno'),
        (5, '⭐⭐⭐⭐⭐ Excelente'),
    ]
    
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given', verbose_name='Revisor')
    reviewed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received', verbose_name='Usuario reseñado')
    
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Calificación')
    comment = models.TextField(max_length=500, blank=True, verbose_name='Comentario')
    
    # Relacionar con transacción (lo crearemos después)
    # transaction = models.ForeignKey('payments.Transaction', on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-created_at']
        unique_together = ['reviewer', 'reviewed']  # Una reseña por par de usuarios
    
    def __str__(self):
        return f"{self.reviewer.username} → {self.reviewed.username}: {self.rating}★"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar reputación del usuario reseñado
        reputation, created = Reputation.objects.get_or_create(user=self.reviewed)
        if self.rating >= 4:
            reputation.positive_reviews += 1
        else:
            reputation.negative_reviews += 1
        reputation.calculate_average_rating()