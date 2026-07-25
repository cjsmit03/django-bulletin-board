"""
Shopping cart functionality using Django sessions.
"""

from .models import Product


class Cart:
    """
    Shopping cart stored in the user's session.
    """

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get("cart", {})

    def add(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1

        self.save()

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True

    def products(self):
        ids = self.cart.keys()
        return Product.objects.filter(id__in=ids)

    def quantities(self):
        return self.cart

    def total(self):
        total = 0

        for product in self.products():
            total += product.price * self.cart[str(product.id)]

        return total

    def count(self):
        return sum(self.cart.values())
        
    def clear(self):
        """
        Remove all items from the cart.
        """
        self.session["cart"] = {}
        self.session.modified = True
        

