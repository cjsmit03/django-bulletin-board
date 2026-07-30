from django.contrib import admin

from .models import (
    Category,
    Order,
    OrderItem,
    Product,
    Review,
    Store,
)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Admin configuration for stores.
    """

    list_display = (
        "name",
        "owner",
        "created_at",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for categories.
    """

    list_display = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for products.
    """

    list_display = (
        "name",
        "store",
        "category",
        "price",
        "stock",
    )

    list_filter = (
        "store",
        "category",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for orders.
    """

    list_display = (
        "id",
        "buyer",
        "created_at",
        "total",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for order items.
    """

    list_display = (
        "order",
        "product",
        "quantity",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for reviews.
    """

    list_display = (
        "product",
        "buyer",
        "rating",
        "verified",
    )
