"""
Tests for the Accounts application.
"""

from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    """
    Basic tests for account pages.
    """

    def test_login_page_loads(self):
        """
        Login page loads successfully.
        """

        response = self.client.get(
            reverse("login")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_register_page_loads(self):
        """
        Register page loads successfully.
        """

        response = self.client.get(
            reverse("register")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_password_reset_page_loads(self):
        """
        Password reset page loads successfully.
        """

        response = self.client.get(
            reverse("password_reset")
        )

        self.assertEqual(
            response.status_code,
            200,
        )
