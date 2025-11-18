from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile, Reputation, Review


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer para el perfil de usuario"""
    class Meta:
        model = Profile
        fields = [
            'avatar', 'bio', 'address', 'city', 'state', 'country',
            'postal_code', 'latitude', 'longitude', 'instagram',
            'facebook', 'whatsapp'
        ]


class ReputationSerializer(serializers.ModelSerializer):
    """Serializer para la reputación"""
    class Meta:
        model = Reputation
        fields = [
            'total_sales', 'total_purchases', 'positive_reviews',
            'negative_reviews', 'average_rating', 'is_verified_seller',
            'is_top_seller'
        ]
        read_only_fields = fields  # Todos son de solo lectura


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para usuario"""
    profile = ProfileSerializer(read_only=True)
    reputation = ReputationSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'role', 'is_verified', 'date_joined',
            'profile', 'reputation'
        ]
        read_only_fields = ['id', 'date_joined', 'is_verified']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'role'
        ]
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden."
            })
        return attrs
    
    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar información del usuario"""
    profile = ProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'email', 'profile'
        ]
    
    def update(self, instance, validated_data):
        """Actualizar usuario y perfil"""
        profile_data = validated_data.pop('profile', None)
        
        # Actualizar usuario
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar perfil si existe
        if profile_data and hasattr(instance, 'profile'):
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """Validar contraseñas"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "Las contraseñas no coinciden."
            })
        return attrs
    
    def validate_old_password(self, value):
        """Verificar que la contraseña actual sea correcta"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer para reseñas"""
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    reviewed_username = serializers.CharField(source='reviewed.username', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewer_username', 'reviewed',
            'reviewed_username', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at']
    
    def create(self, validated_data):
        """Crear reseña y actualizar reputación"""
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)