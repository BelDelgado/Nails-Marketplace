import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User, Profile, Reputation

print("🔧 Limpiando perfiles duplicados...")

# Para cada usuario, asegurarse de que tenga solo 1 Profile y 1 Reputation
for user in User.objects.all():
    # Profile
    profiles = Profile.objects.filter(user=user)
    if profiles.count() > 1:
        print(f"❌ Usuario {user.username} tiene {profiles.count()} profiles")
        # Mantener el primero, borrar el resto
        profiles.exclude(id=profiles.first().id).delete()
        print(f"✅ Limpiado")
    elif profiles.count() == 0:
        Profile.objects.create(user=user)
        print(f"➕ Creado profile para {user.username}")
    
    # Reputation
    reputations = Reputation.objects.filter(user=user)
    if reputations.count() > 1:
        print(f"❌ Usuario {user.username} tiene {reputations.count()} reputations")
        reputations.exclude(id=reputations.first().id).delete()
        print(f"✅ Limpiado")
    elif reputations.count() == 0:
        Reputation.objects.create(user=user)
        print(f"➕ Creado reputation para {user.username}")

print("\n✅ Base de datos limpia")