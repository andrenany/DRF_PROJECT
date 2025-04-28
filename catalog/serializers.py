from rest_framework import serializers
from .models import Category, Product, PriceHistory, Branch, BranchInventory

class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent']

class PriceHistorySerializer(serializers.ModelSerializer):
    """Serializer para historial de precios"""
    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'date']

class ProductSerializer(serializers.ModelSerializer):
    """Serializer para productos"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'price', 'stock', 
                  'category', 'category_name', 'brand', 'model', 
                  'created_at', 'updated_at', 'price_history']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Crear producto
        product = Product.objects.create(**validated_data)
        
        # Registrar precio inicial en historial
        PriceHistory.objects.create(
            product=product,
            price=validated_data['price']
        )
        
        return product
    
    def update(self, instance, validated_data):
        # Verificar si el precio ha cambiado
        if 'price' in validated_data and instance.price != validated_data['price']:
            # Registrar nuevo precio en historial
            PriceHistory.objects.create(
                product=instance,
                price=validated_data['price']
            )
        
        # Actualizar el producto
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance

class BranchSerializer(serializers.ModelSerializer):
    """Serializer para sucursales"""
    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'phone', 'email', 'region', 'city']

class BranchInventorySerializer(serializers.ModelSerializer):
    """Serializer para inventario de sucursales"""
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    
    class Meta:
        model = BranchInventory
        fields = ['id', 'branch', 'branch_name', 'product', 'product_name', 
                  'product_code', 'stock']