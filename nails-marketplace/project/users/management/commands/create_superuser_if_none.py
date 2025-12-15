from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = 'Crea un superusuario si no existe ninguno'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
            email = config('DJANGO_SUPERUSER_EMAIL', default='admin@example.com')
            password = config('DJANGO_SUPERUSER_PASSWORD', default='changeme123')
            
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'✓ Superusuario creado: {username}'))
        else:
            self.stdout.write(self.style.WARNING('✓ Ya existe un superusuario'))