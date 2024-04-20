from rest_framework import status
from rest_framework.generics import CreateAPIView, ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.rest.serializers import CartSerializer, CartItemSerializer
from product.models import Product
from cart.models import Cart, CartItem
from rest_framework.status import *


class CartListCreate(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user.id
        query_set = Cart.objects.filter(user_id=user).first()
        serializer = CartSerializer(query_set)
        return Response(serializer.data)


class AddToCartView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        user = request.user.id
        data = request.data.copy()
        cart = Cart.objects.filter(
            user_id=user).first()
        data['cart'] = cart.id
        product_id = data['product']
        quantity = data['quantity']

        instance = CartItem.objects.filter(
            product_id=product_id, cart_id=cart.id).first()
        print('quantity', quantity)

        if instance:
            if quantity == 0:
                 instance.delete()
            else :      
                if quantity:
                    instance.quantity = quantity
                else:
                    instance.quantity += 1
                instance.save()
            return Response({'message': 'Product Already added.'}, status=status.HTTP_201_CREATED)
        else:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            return Response({'message': 'Added to cart'}, status=status.HTTP_201_CREATED)


class RemoveCartItem(DestroyAPIView):
    def get_serializer_class(self):
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
