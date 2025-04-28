from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from catalog.models import Category, Product, PriceHistory, Branch, BranchInventory

class ModelStrRepresentationTests(TestCase):
    def setUp(self):
        # Configuración inicial común para todos los tests
        self.category = Category.objects.create(name="Herramientas", description="Categoría de herramientas")
        
        self.product = Product.objects.create(
            code="PROD001",
            name="Martillo",
            description="Martillo de acero",
            price=Decimal('15.99'),
            stock=50,
            category=self.category,
            brand="Truper",
            model="M-200"
        )
        
        self.branch = Branch.objects.create(
            name="Sucursal Central",
            address="Av. Principal 123",
            region="Metropolitana",
            city="Santiago"
        )
        
        self.price_history = PriceHistory.objects.create(
            product=self.product,
            price=Decimal('14.99'),
            date=timezone.now()
        )
        
        self.branch_inventory = BranchInventory.objects.create(
            branch=self.branch,
            product=self.product,
            stock=25
        )

    def test_category_str_representation(self):
        """Test para verificar __str__ de Category"""
        self.assertEqual(str(self.category), "Herramientas")

    def test_product_str_representation(self):
        """Test para verificar __str__ de Product"""
        expected_str = "Martillo (PROD001)"
        self.assertEqual(str(self.product), expected_str)

    def test_price_history_str_representation(self):
        """Test para verificar __str__ de PriceHistory"""
        date_str = self.price_history.date.strftime('%Y-%m-%d')
        expected_str = f"Martillo: 14.99 ({date_str})"
        self.assertEqual(str(self.price_history), expected_str)

    def test_branch_str_representation(self):
        """Test para verificar __str__ de Branch"""
        expected_str = "Sucursal Central - Santiago"
        self.assertEqual(str(self.branch), expected_str)

    def test_branch_inventory_str_representation(self):
        """Test para verificar __str__ de BranchInventory"""
        expected_str = "Martillo en Sucursal Central: 25"
        self.assertEqual(str(self.branch_inventory), expected_str)