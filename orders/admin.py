from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('product', 'quantity', 'unit_price', 'subtotal')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'status', 'total', 'payment_method', 'delivery_type')
    list_filter = ('status', 'payment_method', 'delivery_type', 'branch')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('order_date', 'total')
    inlines = (OrderItemInline,)
    fieldsets = (
        (None, {'fields': ('user', 'status')}),
        ('Información de Pago', {'fields': ('total', 'payment_method', 'payment_id')}),
        ('Información de Entrega', {'fields': ('delivery_type', 'delivery_address', 'branch')}),
        ('Fechas', {'fields': ('order_date',)}),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('order__status',)
    search_fields = ('product__name', 'product__code', 'order__user__email')

# Register your models here.
