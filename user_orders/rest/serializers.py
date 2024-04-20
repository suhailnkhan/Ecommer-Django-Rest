# serializers.py
from rest_framework import serializers
from user_orders.models import Order, OrderItem
from product.rest.serializers import ProductListSerializer
from order_payments.models import Payment
from order_payments.rest.serializers import PaymentSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()  # Assuming you have a ProductSerializer

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    payment_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj.id)
        order_items_sr = OrderItemSerializer(order_items, many=True)
        serialized_items = []
        for product_data in order_items_sr.data:
            serialized_items.append(product_data)
        return serialized_items

    def get_payment_details(self, obj):
        payment = Payment.objects.filter(order=obj.id).first()

        if payment:
            serializer = PaymentSerializer(payment)
            return serializer.data

        return None
