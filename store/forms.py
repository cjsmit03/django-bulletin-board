"""
Forms for the Store application.
"""

from django import forms

from .models import Product, Review, Store, Category


class StoreForm(forms.ModelForm):
    """
    Form used to create and update stores.
    """

    class Meta:
        """
        Store form configuration.
        """

        model = Store

        fields = (
            "name",
            "description",
        )


class ProductForm(forms.ModelForm):
    """
    Form used to create and update products.
    """

    class Meta:
        """
        Product form configuration.
        """

        model = Product

        fields = (
            "store",
            "category",
            "name",
            "description",
            "price",
            "stock",
        )

    def __init__(self, *args, **kwargs):
        """
        Restrict store selection to stores owned by the user.
        """
        user = kwargs.pop("user", None)

        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields["store"].queryset = Store.objects.filter(
                owner=user
            )


class ReviewForm(forms.ModelForm):
    """
    Form for submitting a product review.
    """

    class Meta:
        """
        Review form configuration.
        """

        model = Review

        fields = (
            "rating",
            "comment",
        )


class CategoryForm(forms.ModelForm):
    """
    Form used to create categories.
    """

    class Meta:
        """
        Category form configuration.
        """

        model = Category

        fields = ["name"]
