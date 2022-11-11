from django.contrib import admin
from decimal import Decimal
from .models import Product, Collection, Promotion

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


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    search_fields = ['discount']
