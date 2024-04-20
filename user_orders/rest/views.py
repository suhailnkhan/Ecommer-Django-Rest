from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from user_orders.rest.serializers import OrderSerializer, OrderItemSerializer
from user_orders.models import Order, OrderItem
from rest_framework.status import *
from cart.models import Cart, CartItem
from cart.rest.serializers import CartItemSerializer
import json
from collections import OrderedDict


def calculate_total_amount(self, cart_items):
    total_price = 0
    for c in cart_items:
        qnty = c.quantity  # Remove the comma
        price = c.product.price
        item_total = qnty * int(price)
        total_price += item_total  # No need to convert item_total to int here
    # Convert total_price to int once outside the loop
    total_price = int(total_price)
    # loop over items and get total amount
    return total_price


class OrderListCreate(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user = self.request.user.id
        data['user'] = self.request.user.id
        cart = Cart.objects.filter(
            user_id=user).first()
        cart_items = CartItem.objects.filter(cart_id=cart.id)
        data['user'] = user
        total_amount = calculate_total_amount(self, cart_items)
        data['total_amount'] = total_amount
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance:
            try:
                order_item_instances = []
                for cart_item in cart_items:
                    order_item_instances.append(OrderItem(
                        order=instance,
                        quantity=cart_item.quantity,
                        product=cart_item.product
                    ))
                    OrderItem.objects.bulk_create(order_item_instances)
            except Exception as e:
                Order.objects.filter(id=instance.id).delete()
                return Response({'Message': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':  "Order Placed Successfully "}, status=status.HTTP_201_CREATED)



