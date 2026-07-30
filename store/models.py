"""
Database models for the Store application.
"""

from django.contrib.auth.models import User
from django.db import models


class Store(models.Model):
    """
    Represents a vendor's store.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stores",
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """
        Return the store name.
        """
        return self.name


class Category(models.Model):
    """
    Product category.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        """
        Return the category name.
        """
        return self.name


class Product(models.Model):
    """
    Store product.
    """

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    stock = models.PositiveIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """
        Return the product name.
        """
        return self.name


class Order(models.Model):
    """
    Represents a completed order.
    """

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        """
        Return the order identifier.
        """
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """
    Represents a product purchased in an order.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        """
        Return the product name.
        """
        return self.product.name


class Review(models.Model):
    """
    Product review left by a buyer.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    verified = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """
        Return the product and buyer information.
        """
        return f"{self.product.name} - {self.buyer.username}"
