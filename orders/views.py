from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from users.models import User

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.select_related('user', 'branch').prefetch_related('items')
        
        if user.user_type == User.UserType.CLIENTE:
            return queryset.filter(user=user)
        return queryset

    def get_serializer_class(self):
        if self.action in ['create']:
            return OrderCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Asignar el usuario autenticado como dueño del pedido
        order = serializer.save(user=request.user)
        
        # Serializar la respuesta con el formato completo
        response_serializer = OrderSerializer(order)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.OrderStatus.PENDING:
            return Response(
                {'detail': 'Solo se pueden aprobar pedidos pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = Order.OrderStatus.APPROVED
        order.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.OrderStatus.PENDING:
            return Response(
                {'detail': 'Solo se pueden rechazar pedidos pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Devolver productos al stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        order.status = Order.OrderStatus.REJECTED
        order.save()
        return Response({'status': 'rejected'})