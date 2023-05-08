from rest_framework import serializers
from .models import Cart, Order
from ShopApp.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    item = ProductSerializer()
    class Meta:
        model = Cart
        fields = ('id', 'item', 'quantity', 'purchased')

class OrderSerializer(serializers.ModelSerializer):
    orderitems = CartSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'ordered', 'orderitems')

class AddToCartSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

class RemoveFromCartSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

class IncreaseCartSerializer(serializers.Serializer):
    pk = serializers.IntegerField()

class DecreaseCartSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
