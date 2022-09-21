from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

from .models import *


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for price objects."""

    class Meta:
        model = Price
        fields = "__all__"

    # return price amount in naira or dollar value to frontend
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['amount'] = instance.amount / 100
        return representation


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category objects."""

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects."""

    price = PriceSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order objects."""

    user = UserDetailsSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
