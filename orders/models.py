from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from catalog.models import Product, Branch

class Order(models.Model):
    """Modelo de pedido"""
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', _('Pendiente')
        APPROVED = 'APPROVED', _('Aprobado')
        REJECTED = 'REJECTED', _('Rechazado')
        IN_PREPARATION = 'IN_PREPARATION', _('En Preparación')
        READY_FOR_DELIVERY = 'READY_FOR_DELIVERY', _('Listo para Entrega')
        DELIVERED = 'DELIVERED', _('Entregado')
    
    class PaymentMethod(models.TextChoices):
        DEBIT = 'DEBIT', _('Débito')
        CREDIT = 'CREDIT', _('Crédito')
        TRANSFER = 'TRANSFER', _('Transferencia')
    
    class DeliveryType(models.TextChoices):
        STORE_PICKUP = 'STORE_PICKUP', _('Retiro en Tienda')
        HOME_DELIVERY = 'HOME_DELIVERY', _('Despacho a Domicilio')
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_("User")
    )
    order_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Order Date"))
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name=_("Status")
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        verbose_name=_("Payment Method")
    )
    delivery_type = models.CharField(
        max_length=15,
        choices=DeliveryType.choices,
        verbose_name=_("Delivery Type")
    )
    delivery_address = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Delivery Address")
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Total")
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name=_("Branch")
    )
    payment_id = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name=_("Payment ID")
    )
    
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ['-order_date']
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.user.get_full_name}"

class OrderItem(models.Model):
    """Elementos individuales de un pedido"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_("Order")
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_("Product")
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantity")
    )
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Unit Price")
    )
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name=_("Subtotal")
    )
    
    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def save(self, *args, **kwargs):
        """Calcular automáticamente el subtotal"""
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

# Create your models here.
