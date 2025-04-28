from rest_framework import serializers
from .models import Order, OrderItem
from catalog.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer para items de pedido"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_code', 
                  'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['subtotal']

class OrderSerializer(serializers.ModelSerializer):
    """Serializer para pedidos"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'order_date', 'status', 
                  'payment_method', 'delivery_type', 'delivery_address', 
                  'total', 'branch', 'payment_id', 'items']
        read_only_fields = ['id', 'order_date', 'total']

class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear pedidos"""
    items = serializers.ListField(
        child=serializers.DictField(), 
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['user', 'payment_method', 'delivery_type', 'delivery_address', 
                  'branch', 'items']
    
    def validate(self, attrs):
        # Verificar que la dirección de entrega esté presente si es despacho a domicilio
        if attrs['delivery_type'] == Order.DeliveryType.HOME_DELIVERY and not attrs.get('delivery_address'):
            raise serializers.ValidationError(
                {"delivery_address": "La dirección de entrega es obligatoria para despacho a domicilio."}
            )
        
        # Verificar items del pedido
        items = attrs.pop('items')
        if not items:
            raise serializers.ValidationError({"items": "El pedido debe tener al menos un producto."})
        
        # Verificar que los productos existan y tengan stock suficiente
        validated_items = []
        total = 0
        
        for item in items:
            try:
                product_id = item['product']
                quantity = int(item['quantity'])
                
                if quantity <= 0:
                    raise serializers.ValidationError({"quantity": f"La cantidad debe ser mayor que cero para {product_id}."})
                
                product = Product.objects.get(id=product_id)
                
                if product.stock < quantity:
                    raise serializers.ValidationError({"stock": f"Stock insuficiente para {product.name}. Disponible: {product.stock}"})
                
                 # Calcular subtotal
                unit_price = product.price
                subtotal = unit_price * quantity
                total += subtotal
                
                validated_items.append({ 'product': product, 'quantity': quantity,'unit_price': unit_price,'subtotal': subtotal})
                
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product": f"Producto con ID {product_id} no existe."})
            except KeyError as e:
                raise serializers.ValidationError({str(e): f"Este campo es requerido para cada item."})
        
        # Guardar los items validados para usarlos en create()
        attrs['items'] = validated_items
        attrs['total'] = total
        
        return attrs
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total = validated_data.pop('total')
        
        # Crear el pedido
        order = Order.objects.create(
            total=total,
            status=Order.OrderStatus.PENDING,
            **validated_data
        )
        
        # Crear los items del pedido
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                **item_data
            )
            
            # Actualizar stock del producto
            product = item_data['product']
            product.stock -= item_data['quantity']
            product.save()
        
        return order