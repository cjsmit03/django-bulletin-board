"""
Unit tests for the Store application.
"""

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Order, Product, Store


class StoreTests(TestCase):
    """
    Tests for the main eCommerce functionality.
    """

    def setUp(self):
        """
        Create test data.
        """

        Group.objects.get_or_create(name="Vendor")
        Group.objects.get_or_create(name="Customer")

        self.vendor = User.objects.create_user(
            username="vendor",
            password="password123",
        )

        self.customer = User.objects.create_user(
            username="customer",
            password="password123",
        )

        self.category = Category.objects.create(
            name="Electronics",
        )

        self.store = Store.objects.create(
            name="Test Store",
            description="Test Store Description",
            owner=self.vendor,
        )

        self.product = Product.objects.create(
            store=self.store,
            category=self.category,
            name="Gaming Mouse",
            description="RGB Gaming Mouse",
            price=499.99,
            stock=10,
        )

    def test_home_page(self):
        """
        Home page loads successfully.
        """

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_product_detail(self):
        """
        Product detail page loads successfully.
        """

        response = self.client.get(
            reverse(
                "product_detail",
                args=[self.product.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertContains(
            response,
            "Gaming Mouse",
        )

    def test_add_to_cart(self):
        """
        Product can be added to the cart.
        """

        response = self.client.post(
            reverse(
                "add_to_cart",
                args=[self.product.pk],
            )
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_store_requires_login(self):
        """
        Store pages require login.
        """

        response = self.client.get(
            reverse("store_list")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_vendor_login(self):
        """
        Vendor can log in.
        """

        logged_in = self.client.login(
            username="vendor",
            password="password123",
        )

        self.assertTrue(logged_in)

    def test_customer_login(self):
        """
        Customer can log in.
        """

        logged_in = self.client.login(
            username="customer",
            password="password123",
        )

        self.assertTrue(logged_in)

    def test_checkout_creates_order(self):
        """
        Checkout creates an order.
        """

        self.client.login(
            username="customer",
            password="password123",
        )

        session = self.client.session

        session["cart"] = {
            str(self.product.id): 1,
        }

        session.save()

        self.client.get(
            reverse("checkout")
        )

        self.assertEqual(
            Order.objects.count(),
            1,
        )

    def test_customer_cannot_create_store(self):
        """
        Ensure customers cannot create stores.
        """

        customer_group = Group.objects.get(name="Customer")
        self.customer.groups.add(customer_group)

        self.client.login(
            username="customer",
            password="password123",
        )

        response = self.client.get(
            reverse("store_create")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_customer_cannot_create_product(self):
        """
        Ensure customers cannot create products.
        """

        customer_group = Group.objects.get(name="Customer")
        self.customer.groups.add(customer_group)

        self.client.login(
            username="customer",
            password="password123",
        )

        response = self.client.get(
            reverse("product_create")
        )

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_vendor_can_access_store_creation(self):
        """
        Ensure vendors can access the store creation page.
        """

        vendor_group = Group.objects.get(name="Vendor")
        self.vendor.groups.add(vendor_group)

        self.client.login(
            username="vendor",
            password="password123",
        )

        response = self.client.get(
            reverse("store_create")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_vendor_can_access_product_creation(self):
        """
        Ensure vendors can access the product creation page.
        """

        vendor_group = Group.objects.get(name="Vendor")
        self.vendor.groups.add(vendor_group)

        self.client.login(
            username="vendor",
            password="password123",
        )

        response = self.client.get(
            reverse("product_create")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_category_creation(self):
        """
        Ensure categories can be created successfully.
        """

        category = Category.objects.create(
            name="Computers",
        )

        self.assertEqual(
            category.name,
            "Computers",
        )
