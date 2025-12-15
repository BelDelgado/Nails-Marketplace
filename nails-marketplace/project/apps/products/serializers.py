from rest_framework import serializers
from .models import Category, Product, ProductImage
from apps.users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías"""
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 'products_count']
        read_only_fields = ['id']
    
    def get_products_count(self, obj):
        """Contar productos activos en la categoría"""
        return obj.products.filter(status='available').count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer para imágenes de productos"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order']
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de productos"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    primary_image = serializers.SerializerMethodField()

    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'product_type', 'condition', 'status',
            'category_name', 'seller_username', 'primary_image', 'city',
            'views', 'created_at'
        ]
        read_only_fields = ['id', 'views', 'created_at']
    
    def get_primary_image(self, obj):
        """Obtener imagen principal del producto"""
        # Primero buscar imagen marcada como principal
        primary_image = obj.images.filter(is_primary=True).first()
        
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        
        # Si no hay imagen principal, tomar la primera imagen disponible
        first_image = obj.images.first()
        if first_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(first_image.image.url)
            return first_image.image.url
        
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para detalle de producto"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    seller = UserSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'category_id', 'title', 'description',
            'product_type', 'condition', 'status', 'price', 'stock',
            'brand', 'color', 'size', 'city', 'state',
            'latitude', 'longitude', 'views',
            'images', 'is_owner',
            'created_at', 'updated_at', 'expires_at'
        ]
        read_only_fields = [
            'id', 'seller', 'views', 
            'created_at', 'updated_at'
        ]
    
    def get_is_owner(self, obj):
        """Verificar si el usuario actual es el propietario"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.seller == request.user
        return False


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer para crear y actualizar productos"""
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'title', 'description', 'product_type',
            'condition', 'status', 'price', 'stock', 'brand', 'color',
            'size', 'city', 'state', 'latitude', 'longitude',
            'expires_at', 'images', 'uploaded_images'
        ]
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """Crear producto con imágenes"""
        uploaded_images = validated_data.pop('uploaded_images', [])
        validated_data['seller'] = self.context['request'].user
        
        product = Product.objects.create(**validated_data)
        
        # Crear imágenes
        for index, image in enumerate(uploaded_images):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(index == 0),
                order=index
            )
        
        return product
    
    def update(self, instance, validated_data):
        """Actualizar producto"""
        uploaded_images = validated_data.pop('uploaded_images', [])
        
        # Actualizar campos del producto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Agregar nuevas imágenes si existen
        if uploaded_images:
            current_images_count = instance.images.count()
            for index, image in enumerate(uploaded_images):
                ProductImage.objects.create(
                    product=instance,
                    image=image,
                    order=current_images_count + index
                )
        
        return instance