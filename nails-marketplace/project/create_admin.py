import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

if not User.objects.filter(is_superuser=True).exists():
    username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
    email = config('DJANGO_SUPERUSER_EMAIL', default='admin@example.com')
    password = config('DJANGO_SUPERUSER_PASSWORD', default='changeme123')
    
    User.objects.create_superuser(username, email, password)
    print(f'✓ Superusuario creado: {username}')
else:
    print('✓ Ya existe un superusuario')