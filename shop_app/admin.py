from django.contrib import admin
from .models import User, Product, Order, Cart, CartItem
from django.utils.safestring import mark_safe


@admin.action(description="Сбросить количество товаров")
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'image_tag']

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="100" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

    ordering = ['category', '-quantity']
    list_filter = ['name', 'price']
    search_fields = ['name', 'description']
    search_help_text = 'Поиск по имени и описанию продукта'

    actions = [reset_quantity]

    fieldsets = [
        (
            'Товар',
            {
                'classes': ['wide'],
                'fields': ['name', 'image'],
            },
        ),
        (
            'Подробная информация',
            {
                'classes': ['collapse'],
                'description': 'Details',
                'fields': ['description', 'category', ('color', 'size')],
            },
        ),
        (
            'Учетная информация',
            {
                'description': 'Details',
                'fields': [('price', 'quantity')],
            },
        ),

    ]


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    ordering = ['name']
    list_filter = ['name', 'address']
    search_fields = ['name']
    search_help_text = 'Поиск по имени пользователя'

    readonly_fields = ['telephone', 'password']

    fieldsets = [
        (
            'Пользователь',
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Контактная информация',
            {
                'classes': ['collapse'],
                'fields': ['email', 'telephone', 'address'],
            },
        ),
        (
            'Личная информация',
            {
                'classes': ['collapse'],
                'fields': ['password'],
            },
        ),

    ]


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart_item_price']
    ordering = ['cart_item_price']
    list_filter = ['product', 'quantity']
    search_fields = ['product']
    search_help_text = 'Поиск по наименованию товара'

    readonly_fields = ['product', 'quantity', 'cart_item_price']

    fieldsets = [
        (
            'Позиция корзины',
            {
                'classes': ['wide'],
                'fields': ['product', 'quantity', 'cart_item_price'],
            },
        ),
    ]


class CartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']
    ordering = ['products']
    list_filter = ['products']
    search_fields = ['products']
    search_help_text = 'Поиск по наименованию товара'

    readonly_fields = ['user', 'products']

    filter_vertical = ['products']

    fieldsets = [
        (
            'Корзина',
            {
                'classes': ['wide'],
                'fields': ['user', 'products'],
            },
        ),
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'order_date', 'status']
    ordering = ['-order_date']
    list_filter = ['total_price', 'order_date', 'status']
    search_fields = ['user']
    search_help_text = 'Поиск по имени пользователя'

    readonly_fields = ['products','order_date']

    filter_horizontal = ['products']

    fieldsets = [
        (
            'Заказ',
            {
                'classes': ['wide'],
                'fields': ['user', 'total_price', 'order_date', 'status'],
            },
        ),
        (
            'Товары',
            {
                'classes': ['collapse'],
                'fields': ['products'],
            },
        ),
        (
            'Детали',
            {
                'classes': ['collapse'],
                'fields': ['delivery_address', 'payment_option'],
            },
        ),
    ]


admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
