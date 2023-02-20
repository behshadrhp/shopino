from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from decimal import Decimal
from .models import Product, Collection, Promotion, Customer, Order, Address, OrderItem, Cart, CartItem, ProductImage

# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<50', 'Low'),
            ('>50', 'High')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<50':
            return queryset.filter(inventory__lt=50)
        elif self.value() == '<50':
            return queryset.filter(InventoryFilter__gt=50)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price',
                    'net_profit_of_the_product', 'inventory', 'collection', 'last_update']
    list_per_page = 8
    list_editable = ['price', 'inventory']
    list_filter = ['collection', InventoryFilter]
    search_fields = ['title__istartswith']
    actions = ['clear_price', 'clear_inventory']
    fields = ['title', 'description', 'slug', 'price',
              'inventory', 'collection', 'promotions']
    autocomplete_fields = ['collection', 'promotions']
    prepopulated_fields = {
        'slug': ['title'],
    }

    def discount_price(self, product: Product):
        if product.price < 50.00:
            discount = 0.13
            discounted = product.price * Decimal(discount)
            total = product.price - discounted
            return round(total, 2)
        elif product.price > 50.00:
            discount = 0.25
            discounted = product.price * Decimal(discount)
            total = product.price - discounted
            return round(total, 2)

    def net_profit_of_the_product(self, product: Product):
        discount = self.discount_price(product)
        profit = Decimal(product.price) - discount
        return profit

    @admin.action(description='Clear Price')
    def clear_price(self, request, queryset):
        update_price = queryset.update(price=0)
        self.message_user(
            request,
            f'The desired price has been removed'
        )

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        update_inventory = queryset.update(inventory=0)
        self.message_user(
            request,
            f'inventory has been removed'
        )

    class Meta:
        ordering = ['last_update', 'inventory']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone',
                    'birth_day', 'customer_order', 'membership']
    list_per_page = 10
    list_editable = ['membership', 'phone']
    list_filter = ['membership']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']

    def full_name(self, customer: Customer):
        return f'{customer.user}'

    def email(self, customer: Customer):
        return f'{customer.user.email}'

    def customer_order(self, order: Order):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': order.id
            })
        )
        return format_html(f'<a href="{url}">{order.customer_order}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_order=Count('order')
        )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'payment_status', 'placed_at']
    list_per_page = 10
    list_editable = ['payment_status']
    list_filter = ['payment_status']
    search_fields = ['customer__first_name__istartswith',
                     'customer__last_name__istartswith']
    autocomplete_fields = ['customer']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'city', 'street']
    list_per_page = 10
    list_editable = ['city', 'street']
    search_fields = ['customer__first_name__istartswith',
                     'customer__last_name__istartswith']
    autocomplete_fields = ['customer']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_product', 'product_count']
    list_per_page = 10
    list_editable = ['featured_product']
    autocomplete_fields = ['featured_product']
    search_fields = ['title']

    def product_count(self, collection: Collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html(f'<a href="{url}">{collection.product_count}</a>')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_editable = ['quantity']
    list_per_page = 10
    search_fields = ['order__customer__first_name__istartswith',
                     'order__customer__last_name__istartswith']
    autocomplete_fields = ['order', 'product']

    def price(self, order: OrderItem):
        return order.quantity * order.product.price


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart']
    list_per_page = 10
    search_fields = ['product__title__istartswith']
    autocomplete_fields = ['product']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    search_fields = ['discount']
    list_per_page = 10


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass
