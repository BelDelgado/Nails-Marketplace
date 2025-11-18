from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Reputation


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crear automáticamente Profile y Reputation cuando se crea un usuario
    """
    if created:
        Profile.objects.create(user=instance)
        Reputation.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Guardar el perfil cuando se guarda el usuario
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'reputation'):
        instance.reputation.save()