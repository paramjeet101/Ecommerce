from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderListCreateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """create order from cart"""
        cart = Cart.objects.get(user=request.user)
        total = cart.total_amount()

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_address=request.data.get("shipping_address", ""),
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity,
            )

        # clear cart
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        order = Order.objects.get(pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
