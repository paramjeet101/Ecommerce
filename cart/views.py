from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product


def api_response(success, message, data=None, http=200):
    return Response({
        "success": success,
        "message": message,
        "data": data or {}
    }, status=http)


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.get_unpaid_cart(request.user)
            return api_response(True, "Cart fetched successfully", CartSerializer(cart).data)

        except Exception as e:
            return api_response(False, f"Error fetching cart: {str(e)}", http=500)


class AddToCartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get("product_id")
            quantity = request.data.get("quantity")

            if not product_id:
                return api_response(False, "product_id is required", http=400)

            if not quantity or int(quantity) <= 0:
                return api_response(False, "quantity must be greater than 0", http=400)

            product = get_object_or_404(Product, id=product_id)

            cart = Cart.get_unpaid_cart(request.user)

            # Existing item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                user=request.user,
                product=product,
            )

            cart_item.quantity = int(quantity)
            cart_item.save()

            return api_response(
                True,
                "Item added to cart successfully",
                CartSerializer(cart).data,
                http=201
            )

        except Exception as e:
            return api_response(False, f"Error adding item to cart: {str(e)}", http=500)


class UpdateCartItemAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, item_id):
        try:
            quantity = request.data.get("quantity")

            if not quantity or int(quantity) <= 0:
                return api_response(False, "quantity must be greater than 0", http=400)

            item = get_object_or_404(CartItem, id=item_id, user=request.user)

            item.quantity = int(quantity)
            item.save()

            return api_response(True, "Cart item updated successfully")

        except Exception as e:
            return api_response(False, f"Error updating cart item: {str(e)}", http=500)


class RemoveCartItemAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = get_object_or_404(CartItem, id=item_id, user=request.user)
            item.delete()

            return api_response(True, "Item removed from cart successfully")

        except Exception as e:
            return api_response(False, f"Error removing item: {str(e)}", http=500)


class ClearCartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        try:
            cart = Cart.get_unpaid_cart(request.user)
            cart.items.all().delete()

            return api_response(True, "Cart cleared successfully")

        except Exception as e:
            return api_response(False, f"Error clearing cart: {str(e)}", http=500)
