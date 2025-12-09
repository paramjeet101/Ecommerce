from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer
from .models import UserProfile


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


class RegisterAPI(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)

            return Response({
                "success": True,
                "message": "User registered successfully",
                "tokens": tokens,
                "user": UserSerializer(user).data
            }, status=201)

        return Response(serializer.errors, status=400)


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"detail": "Email & password required"}, status=400)

        user = authenticate(username=email, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials"}, status=401)

        tokens = get_tokens_for_user(user)

        return Response({
            "success": True,
            "message": "Login successful",
            "tokens": tokens,
            "user": UserSerializer(user).data
        })
        

class ProfileAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Profile updated"})
        return Response(serializer.errors, status=400)


class LogoutAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"success": True, "message": "Logged out"})
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)
