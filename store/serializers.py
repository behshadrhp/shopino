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


class CartItemCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title']


class CartItemProductSerializer(serializers.ModelSerializer):
    collection = CartItemCollectionSerializer()

    class Meta:
        model = Product
        fields = ['title', 'price', 'inventory', 'collection', 'last_update']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: CartItem):
        return cart.quantity * cart.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
