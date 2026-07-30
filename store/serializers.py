from rest_framework import serializers

from .models import Product, Review, Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Store model.
    """

    class Meta:
        """
        Store serializer configuration.
        """

        model = Store
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """

    class Meta:
        """
        Product serializer configuration.
        """

        model = Product
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """

    class Meta:
        """
        Review serializer configuration.
        """

        model = Review
        fields = "__all__"
