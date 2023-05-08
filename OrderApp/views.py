from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages

from .serializers import CartSerializer, OrderSerializer
from ShopApp.models import Product
from OrderApp.models import Cart, Order

User = get_user_model()

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        item = get_object_or_404(Product, pk=pk)
        user = request.user
        cart, created = Cart.objects.get_or_create(item=item, user=user, purchased=False)
        if not created:
            cart.quantity += 1
            cart.save()
            messages.info(request, "This item quantity was updated.")
            return Response(status=status.HTTP_200_OK)
        else:
            order_qs = Order.objects.filter(user=user, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
                order.orderitems.add(cart)
            else:
                order = Order.objects.create(user=user)
                order.orderitems.add(cart)
            messages.info(request, "This item was added to your cart.")
            return Response(status=status.HTTP_201_CREATED)


class CartView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = Order.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            cart_serializer = CartSerializer(carts, many=True)
            order_serializer = OrderSerializer(orders[0])
            data = {
                'carts': cart_serializer.data,
                'order': order_serializer.data
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            messages.warning(request, "You don't have any item in your cart!")
            return Response(status=status.HTTP_204_NO_CONTENT)


class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        item = get_object_or_404(Product, pk=pk)
        user = request.user
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                cart = Cart.objects.filter(item=item, user=user, purchased=False)[0]
                order.orderitems.remove(cart)
                cart.delete()
                messages.warning(request, "This item was removed from your cart")
                return Response(status=status.HTTP_200_OK)
            else:
                messages.info(request, "This item was not in your cart.")
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            messages.info(request, "You don't have an active order")
            return Response(status=status.HTTP_404_NOT_FOUND)


class IncreaseCartView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        item = get_object_or_404(Product, pk=pk)
        user = request.user
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                cart = Cart.objects.filter(item=item, user=user, purchased=False)[0]
                cart.quantity += 1
                cart.save()
                messages.info(request, f"{item.name} quantity has been updated")
                return Response(status=status.HTTP_200_OK)
            else:
                messages.info(request, f"{item.name} is not in your cart")




