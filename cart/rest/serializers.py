from cart.models import Cart, CartItem
from rest_framework import serializers
from product.rest.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    totalItems = serializers.SerializerMethodField()
    isEmpty = serializers.SerializerMethodField()
    totalCartValue = serializers.SerializerMethodField()
    # ProductListSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def get_items(self, obj):
        items = obj.items.all()
        product_serializer = ProductListSerializer(items, many=True)
        serialized_items = []
        for product_data in product_serializer.data:
            quantity = get_quantity_for_product(
                self, obj.id, product_data['id'])
            product_data['quantity'] = quantity
            serialized_items.append(product_data)
        return serialized_items

    def get_totalItems(self, obj):
        items = obj.items.all()
        return len(items)

    def get_isEmpty(self, obj):
        items = obj.items.all()
        return True if len(items) == 0 else False

    def get_totalCartValue(self, obj):
        total_price = 0
        items = obj.items.all()
        for item in items:
            total_price += item.price * get_quantity_for_product(
                self, obj.id, item.id)
        return total_price


def get_quantity_for_product(self, cart_id, product_id):
    try:
        cart_item = CartItem.objects.filter(
            cart_id=cart_id, product_id=product_id).first()
        return cart_item.quantity
    except CartItem.DoesNotExist:
        return 0
