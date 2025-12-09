from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Coupon
from .serializers import CouponSerializer


class CouponApplyAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")

        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
        except Coupon.DoesNotExist:
            return Response({"success": False, "message": "Invalid Coupon"}, status=400)

        if not coupon.is_valid():
            return Response({"success": False, "message": "Coupon expired"}, status=400)

        serializer = CouponSerializer(coupon)
        return Response({"success": True, "data": serializer.data})
