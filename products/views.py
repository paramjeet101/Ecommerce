from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Category, Product
from .serializers import CategorySerializer,ProductSerializer


class CategoryListCreateAPI(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        print(request.user)
        queryset = Category.objects.filter(is_active=True).order_by("display_order")
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPI(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_object(self, pk):
        return Category.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response({"message": "Category deleted"})
    

class ProductListCreateAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = Product.objects.filter(is_active=True)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    

class ProductDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return Product.objects.get(pk=pk)

    def get(self, request, pk):
        serializer = ProductSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = ProductSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response({"message": "Product deleted"})
