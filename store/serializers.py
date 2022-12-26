from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem
from decimal import Decimal


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price',
                  'discount', 'profit', 'inventory', 'collection', 'last_update']

    discount = serializers.SerializerMethodField(method_name='discount_price')
    profit = serializers.SerializerMethodField(
        method_name='profit_of_the_product')

    def discount_price(self, product: Product):
        if product.price <= 50.00:
            discount = 0.13
            discounted = product.price * Decimal(discount)
            total = product.price - discounted
            return round(total, 2)
        elif product.price >= 50.00:
            discount = 0.25
            discounted = product.price * Decimal(discount)
            total = product.price - discounted
            return round(total, 2)

    def profit_of_the_product(self, product: Product):
        discount = self.discount_price(product)
        profit = product.price - Decimal(discount)
        return round(profit, 2)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']
