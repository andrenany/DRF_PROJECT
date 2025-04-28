
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProductViewSet,
    PriceHistoryViewSet, BranchViewSet,
    BranchInventoryViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'inventory', BranchInventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_pk>/price-history/', 
         PriceHistoryViewSet.as_view({'get': 'list'}), 
         name='product-price-history'),
]