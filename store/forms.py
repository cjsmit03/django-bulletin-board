"""
Forms for the Store application.
"""

from django import forms

from .models import Product, Review, Store


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store

        fields = (
            "name",
            "description",
        )


class ProductForm(forms.ModelForm):
    class Meta:
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
        model = Review

        fields = (
            "rating",
            "comment",
        )
