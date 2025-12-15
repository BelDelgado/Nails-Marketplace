import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
email = config('DJANGO_SUPERUSER_EMAIL', default='admin@example.com')
password = config('DJANGO_SUPERUSER_PASSWORD', default='changeme123')

# Verificar si existe el usuario
user = User.objects.filter(username=username).first()

if user:
    # Si existe, actualizar contraseña por si acaso
    if not user.is_superuser:
        user.is_superuser = True
        user.is_staff = True
        user.save()
    user.set_password(password)
    user.save()
    print(f'✓ Superusuario actualizado: {username}')
else:
    # Si no existe, crearlo
    try:
        User.objects.create_superuser(username, email, password)
        print(f'✓ Superusuario creado: {username}')
    except Exception as e:
        print(f'⚠ Error al crear superusuario: {e}')
        print('✓ Intentando recuperar usuario existente...')
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        print(f'✓ Superusuario recuperado: {username}')