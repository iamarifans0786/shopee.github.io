from rest_framework import serializers
from django.contrib.auth.models import User
from product.models import ProductCategory, Product, ProductImage
from cart.models import Cart
from user_profile.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user Profile"""

    class Meta:
        model = UserProfile
        fields = ["id", "user", "mobile", "address", "profile_image"]


class UserAuthSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "user_profile",
        ]
        depth=1
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """Override model's serializers create(POST) method"""
        user = User.objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """Override model's serializers update(PUT, PATCH) method"""
        if validated_data.get("username"):
            instance.username = validated_data["username"]
        if validated_data.get("first_name"):
            instance.first_name = validated_data["first_name"]
        if validated_data.get("last_name"):
            instance.last_name = validated_data["last_name"]
        if validated_data.get("email"):
            instance.email = validated_data["email"]
        if validated_data.get("password"):
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer for product category"""

    class Meta:
        model = ProductCategory
        fields = ["name", "slug", "image"]


class ProductCategorySerializer(serializers.ModelSerializer):
    """Serializer for product category"""

    class Meta:
        model = ProductCategory
        fields = ["name", "slug", "image"]


class ProductImagesSerializer(serializers.ModelSerializer):
    """Product Multiple images Serializer class for Product Serializer"""

    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductSerializer(serializers.ModelSerializer):
    """Product Model Serializer"""

    product_images = ProductImagesSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "product_category",
            "brand",
            "name",
            "slug",
            "cover_image",
            "price",
            "description",
            "variation",
            "tags",
            "product_images",
        ]
        depth = 1


class CartSerializer(serializers.ModelSerializer):
    """Cart model serializer"""

    sub_total = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "product",
            "variation",
            "quantity",
            "sub_total",
        ]
        depth = 1
