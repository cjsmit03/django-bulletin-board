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

    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
    )

    class Meta:
        """
        Registration form configuration.
        """

        model = User

        fields = (
            "username",
            "email",
            "role",
            "password1",
            "password2",
        )

    def clean_email(self):
        """
        Ensure the email address is unique.
        """

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email
