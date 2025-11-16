from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Profile, Review
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    ReviewSerializer,
    ProfileSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para usuarios
    
    Endpoints:
    - POST /api/v1/users/register/ - Registrar nuevo usuario
    - GET /api/v1/users/profile/ - Obtener perfil del usuario actual
    - PUT/PATCH /api/v1/users/profile/ - Actualizar perfil
    - POST /api/v1/users/change-password/ - Cambiar contraseña
    - GET /api/v1/users/{id}/ - Ver perfil público de un usuario
    """
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        """Usar diferentes serializers según la acción"""
        if self.action == 'register':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update', 'update_profile']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer
    
    def get_permissions(self):
        """Permisos según la acción"""
        if self.action == 'register':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Registrar nuevo usuario"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': '¡Usuario registrado exitosamente!'
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Obtener o actualizar perfil del usuario actual"""
        user = request.user
        
        if request.method == 'GET':
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        
        # PUT o PATCH
        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'message': 'Perfil actualizado exitosamente'
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario"""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Cambiar contraseña
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        })
    
    @action(detail=True, methods=['get'])
    def public_profile(self, request, pk=None):
        """Ver perfil público de un usuario"""
        user = self.get_object()
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet para reseñas de usuarios
    
    Endpoints:
    - GET /api/v1/reviews/ - Listar reseñas
    - POST /api/v1/reviews/ - Crear reseña
    - GET /api/v1/reviews/{id}/ - Detalle de reseña
    - GET /api/v1/reviews/received/ - Reseñas recibidas
    - GET /api/v1/reviews/given/ - Reseñas dadas
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filtrar reseñas según parámetros"""
        queryset = Review.objects.all()
        
        # Filtrar por usuario reseñado
        reviewed_id = self.request.query_params.get('reviewed', None)
        if reviewed_id:
            queryset = queryset.filter(reviewed_id=reviewed_id)
        
        return queryset.select_related('reviewer', 'reviewed')
    
    @action(detail=False, methods=['get'])
    def received(self, request):
        """Reseñas recibidas por el usuario actual"""
        reviews = Review.objects.filter(reviewed=request.user)
        
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def given(self, request):
        """Reseñas dadas por el usuario actual"""
        reviews = Review.objects.filter(reviewer=request.user)
        
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)