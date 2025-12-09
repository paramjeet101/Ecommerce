from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product


class CartAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key or request.session.create()
            cart, _ = Cart.objects.get_or_create(session_id=session_id)
        return cart

    def get(self, request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        """Add item to cart"""
        product_id = request.data.get("product_id")
        qty = int(request.data.get("quantity", 1))

        cart = self.get_cart(request)
        product = Product.objects.get(id=product_id)

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = qty
        item.save()

        return Response({"message": "Item added to cart"})


class CartRemoveAPI(APIView):

    def post(self, request):
        item_id = request.data.get("item_id")
        CartItem.objects.filter(id=item_id).delete()
        return Response({"message": "Item removed from cart"})
