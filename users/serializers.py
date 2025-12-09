from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True, required=False)
    address = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name", "phone", "address")

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value.lower()

    def create(self, validated_data):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        email = validated_data.get("email")
        password = validated_data.get("password")
        phone = validated_data.pop("phone", "")
        address = validated_data.pop("address", "")

        user = User.objects.create_user(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        profile = UserProfile.objects.create(user=user)
        profile.phone = phone
        profile.address = address
        profile.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="profile.phone", read_only=True)
    address = serializers.CharField(source="profile.address", read_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "phone", "address", "profile_image")

    def get_profile_image(self, obj):
        try:
            return obj.profile.profile_image.url if obj.profile.profile_image else None
        except:
            return None


class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.first_name", required=False)

    class Meta:
        model = UserProfile
        fields = ("phone", "address", "profile_image", "full_name")

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        if "first_name" in user_data:
            instance.user.first_name = user_data["first_name"]
            instance.user.save()

        return super().update(instance, validated_data)
