from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from catalog.models import Product, Branch, Category  # Añadimos Category al import
from orders.models import Order, OrderItem

User = get_user_model()

class OrderModelTests(TestCase):
    def setUp(self):
        # Crear datos de prueba
        self.user = User.objects.create_user(
            email='cliente@example.com',
            first_name='Juan',
            last_name='Perez',
            password='testpass123'
        )
        
        # Primero creamos una categoría
        self.category = Category.objects.create(
            name='Herramientas',
            description='Categoría de herramientas'
        )
        
        self.branch = Branch.objects.create(
            name='Sucursal Principal',
            address='Av. Principal 123',
            region='Metropolitana',
            city='Santiago'
        )
        
        # Ahora creamos el producto con la categoría
        self.product = Product.objects.create(
            code='PROD001',
            name='Martillo',
            description='Martillo de acero',
            price=Decimal('15.99'),
            stock=50,
            category=self.category,  # Añadimos la categoría
            brand='Truper',
            model='M-200'
        )
        
        self.order = Order.objects.create(
            user=self.user,
            status=Order.OrderStatus.PENDING,
            payment_method=Order.PaymentMethod.CREDIT,
            delivery_type=Order.DeliveryType.HOME_DELIVERY,
            total=Decimal('100.00'),
            branch=self.branch
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal('15.99')
        )

    def test_order_str_representation(self):
        """Test para verificar __str__ de Order"""
        expected_str = f"Pedido #{self.order.id} - Juan Perez"
        self.assertEqual(str(self.order), expected_str)

    def test_order_item_str_representation(self):
        """Test para verificar __str__ de OrderItem"""
        expected_str = "2 x Martillo"
        self.assertEqual(str(self.order_item), expected_str)

    def test_order_item_subtotal_calculation(self):
        """Test para verificar el cálculo automático del subtotal"""
        # El subtotal debería ser quantity * unit_price
        expected_subtotal = Decimal('2') * Decimal('15.99')
        self.assertEqual(self.order_item.subtotal, expected_subtotal)
        
        # Verificar que se recalcula al actualizar
        self.order_item.quantity = 3
        self.order_item.save()
        expected_subtotal_updated = Decimal('3') * Decimal('15.99')
        self.assertEqual(self.order_item.subtotal, expected_subtotal_updated)