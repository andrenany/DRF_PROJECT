from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, PriceHistory, Branch, BranchInventory

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    mptt_level_indent = 20

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'stock', 'category', 'brand')
    list_filter = ('category', 'brand')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {'fields': ('code', 'name', 'description')}),
        ('Precio y Stock', {'fields': ('price', 'stock')}),
        ('Categorización', {'fields': ('category', 'brand', 'model')}),
        ('Fechas', {'fields': ('created_at', 'updated_at')}),
    )

class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ('date',)
    can_delete = False

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'date')
    list_filter = ('product', 'date')
    readonly_fields = ('date',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'phone')
    search_fields = ('name', 'city', 'region')
    list_filter = ('region', 'city')

class BranchInventoryInline(admin.TabularInline):
    model = BranchInventory
    extra = 1

@admin.register(BranchInventory)
class BranchInventoryAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'stock')
    list_filter = ('branch',)
    search_fields = ('product__name', 'product__code')

# Register your models here.
