from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    """Categoría de productos con estructura jerárquica"""
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name=_("Parent Category")
    )
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    def __str__(self):
        return self.name

class Product(models.Model):
    """Modelo de producto"""
    code = models.CharField(max_length=20, unique=True, verbose_name=_("Code"))
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Price")
    )
    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"))
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name=_("Category")
    )
    brand = models.CharField(max_length=100, verbose_name=_("Brand"))
    model = models.CharField(max_length=100, verbose_name=_("Model"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    def __str__(self):
        return f"{self.name} ({self.code})"

class PriceHistory(models.Model):
    """Historial de precios de productos"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='price_history',
        verbose_name=_("Product")
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Price")
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    
    class Meta:
        verbose_name = _("Price History")
        verbose_name_plural = _("Price History")
        ordering = ['-date']
    def __str__(self):
        return f"{self.product.name}: {self.price} ({self.date.strftime('%Y-%m-%d')})"

class Branch(models.Model):
    """Sucursales de FERREMAS"""
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    address = models.TextField(verbose_name=_("Address"))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    region = models.CharField(max_length=100, verbose_name=_("Region"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    
    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")
    def __str__(self):
     return f"{self.name} - {self.city}"

class BranchInventory(models.Model):
    """Inventario por sucursal"""
    branch = models.ForeignKey(
        Branch, 
        on_delete=models.CASCADE, 
        related_name='inventory',
        verbose_name=_("Branch")
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='branch_inventory',
        verbose_name=_("Product")
    )
    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stock"))
    
    class Meta:
        verbose_name = _("Branch Inventory")
        verbose_name_plural = _("Branch Inventories")
        unique_together = ('branch', 'product')
    def __str__(self):
        return f"{self.product.name} en {self.branch.name}: {self.stock}"

# Create your models here.
