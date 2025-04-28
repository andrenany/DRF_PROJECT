from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Importa las vistas de tus apps
from users.views import UserViewSet
from catalog.views import (
    CategoryViewSet, 
    ProductViewSet, 
    BranchViewSet,
    BranchInventoryViewSet
)
from orders.views import OrderViewSet

# Configura el router
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"branches", BranchViewSet, basename="branch")
router.register(r"inventory", BranchInventoryViewSet, basename="inventory")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API
    path("api/", include(router.urls)),
    
    # Auth endpoints (separados para mejor organización)
    path("api/auth/", include("users.urls")),
    
    # Documentación API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    
    # URLs específicas de catalog (para relaciones anidadas)
    path("api/catalog/products/<int:product_pk>/price-history/", 
         include("catalog.urls")),
    
    # URLs específicas de orders (para acciones adicionales)
    path("api/orders/<int:pk>/approve/", 
         include("orders.urls")),
    path("api/orders/<int:pk>/reject/", 
         include("orders.urls")),
]