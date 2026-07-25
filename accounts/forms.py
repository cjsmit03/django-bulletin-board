"""
Forms for the Accounts application.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Registration form with a user role.
    """

    ROLE_CHOICES = (
        ("Customer", "Customer"),
        ("Vendor", "Vendor"),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = User

        fields = (
            "username",
            "role",
            "password1",
            "password2",
        )
