"""
Shopping cart functionality using Django sessions.
"""

from .models import Product


class Cart:
    """
    Shopping cart stored in the user's session.
    """

    def __init__(self, request):
        """
        Initialise the shopping cart from the user's session.
        """
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def add(self, product_id):
        """
        Add a product to the shopping cart.
        """
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1

        self.save()

    def remove(self, product_id):
        """
        Remove a product from the shopping cart.
        """
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def save(self):
        """
        Save the shopping cart to the session.
        """
        self.session["cart"] = self.cart
        self.session.modified = True

    def products(self):
        """
        Return all products contained in the cart.
        """
        ids = self.cart.keys()
        return Product.objects.filter(id__in=ids)

    def quantities(self):
        """
        Return the quantities of all products in the cart.
        """
        return self.cart

    def total(self):
        """
        Calculate the total cost of the shopping cart.
        """
        total = 0

        for product in self.products():
            total += product.price * self.cart[str(product.id)]

        return total

    def count(self):
        """
        Return the number of items in the shopping cart.
        """
        return sum(self.cart.values())

    def clear(self):
        """
        Remove all items from the cart.
        """
        self.session["cart"] = {}
        self.session.modified = True
