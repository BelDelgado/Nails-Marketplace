from django import forms
from .models import Product, ProductImage, Category

class ProductForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'product_type', 
            'condition', 'price', 'stock', 'brand', 'color', 
            'size', 'city', 'state'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Ej: Esmalte gel UV rosa pastel'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu producto en detalle...'
            }),
            'product_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': '1'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marca del producto'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Color'
            }),
            'size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tamaño o volumen'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Provincia'
            }),
        }
        labels = {
            'category': 'Categoría *',
            'title': 'Título *',
            'description': 'Descripción *',
            'product_type': 'Tipo',
            'condition': 'Condición *',
            'price': 'Precio (ARS) *',
            'stock': 'Stock *',
            'brand': 'Marca',
            'color': 'Color',
            'size': 'Tamaño/Volumen',
            'city': 'Ciudad',
            'state': 'Provincia',
        }

class ProductImageForm(forms.ModelForm):
    """Formulario para subir imágenes"""
    
    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_primary']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la imagen'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }