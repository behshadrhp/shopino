from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from uuid import uuid4

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE)
    promotions = models.ManyToManyField('Promotion', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_update']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICE = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, unique=True)
    birth_day = models.DateField(null=True, blank=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name',
                    'user__last_name', 'birth_day', 'membership']
        permissions = [
            ('view_history', 'Can view history')
        ]


class Order(models.Model):
    PENDING_STATUS = 'P'
    COMPLETE_STATUS = 'C'
    FAILED_STATUS = 'F'
    PAYMENT_STATUS = [
        (PENDING_STATUS, 'Pending'),
        (COMPLETE_STATUS, 'Complete'),
        (FAILED_STATUS, 'Failed')
    ]

    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PENDING_STATUS)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer} - {self.payment_status}'

    class Meta:
        permissions = [
            ('cancel_order', 'can cancel order')
        ]
        ordering = ['-placed_at']


class Address(models.Model):
    customer = models.OneToOneField(
        'Customer', on_delete=models.CASCADE, primary_key=True)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.customer} - {self.city}'

    class Meta:
        ordering = ['customer', 'city']


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.PROTECT)
    product = models.ForeignKey(
        'Product', on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f'{self.product} - {self.order}'

    class Meta:
        ordering = ['product']


class Cart(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True,
                          editable=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.create_at)

    class Meta:
        ordering = ['-create_at']


class CartItem(models.Model):
    cart = models.ForeignKey(
        'Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self):
        return f'{self.product} - {self.quantity} - {self.cart}'

    class Meta:
        ordering = ['cart']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

    def __str__(self):
        return str(self.discount)

    class Meta:
        ordering = ['discount']


class Review(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
