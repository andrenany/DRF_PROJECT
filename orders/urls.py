from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('orders/<int:pk>/approve/', 
         OrderViewSet.as_view({'post': 'approve'}), 
         name='order-approve'),
    path('orders/<int:pk>/reject/', 
         OrderViewSet.as_view({'post': 'reject'}), 
         name='order-reject'),
] + router.urls