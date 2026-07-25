"""
Views for the Store application.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .models import Product, Store
from decimal import Decimal
from .forms import ProductForm, ReviewForm, StoreForm

from django.core.mail import send_mail

from .models import Order, OrderItem


def home(request):
    products = Product.objects.all()

    return render(
        request,
        "store/home.html",
        {
            "products": products,
        },
    )


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
        },
    )


def add_to_cart(request, pk):
    cart = Cart(request)
    cart.add(pk)
    return redirect("cart")


def remove_from_cart(request, pk):
    cart = Cart(request)
    cart.remove(pk)
    return redirect("cart")


def cart_view(request):
    cart = Cart(request)

    items = []
    total = 0

    for product in cart.products():

        quantity = cart.quantities()[str(product.id)]

        subtotal = quantity * product.price

        total += subtotal

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "store/cart.html",
        {
            "items": items,
            "total": total,
        },
    )


@login_required
def store_list(request):

    stores = Store.objects.filter(owner=request.user)

    return render(
        request,
        "store/store_list.html",
        {
            "stores": stores,
        },
    )


@login_required
def store_create(request):

    if request.method == "POST":

        form = StoreForm(request.POST)

        if form.is_valid():

            store = form.save(commit=False)

            store.owner = request.user

            store.save()

            return redirect("store_list")

    else:

        form = StoreForm()

    return render(
        request,
        "store/store_form.html",
        {
            "form": form,
            "title": "Create Store",
        },
    )


@login_required
def store_update(request, pk):

    store = get_object_or_404(
        Store,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":

        form = StoreForm(
            request.POST,
            instance=store,
        )

        if form.is_valid():

            form.save()

            return redirect("store_list")

    else:

        form = StoreForm(instance=store)

    return render(
        request,
        "store/store_form.html",
        {
            "form": form,
            "title": "Edit Store",
        },
    )


@login_required
def store_delete(request, pk):

    store = get_object_or_404(
        Store,
        pk=pk,
        owner=request.user,
    )

    if request.method == "POST":

        store.delete()

        return redirect("store_list")

    return render(
        request,
        "store/store_delete.html",
        {
            "store": store,
        },
    )
    

@login_required
def product_list(request):
    """
    Display products belonging to the logged-in vendor.
    """
    products = Product.objects.filter(store__owner=request.user)

    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
        },
    )


@login_required
def product_create(request):
    """
    Create a product for one of the vendor's stores.
    """
    if request.method == "POST":

        form = ProductForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            return redirect("product_list")

    else:

        form = ProductForm(user=request.user)

    return render(
        request,
        "store/product_form.html",
        {
            "form": form,
            "title": "Create Product",
        },
    )


@login_required
def product_update(request, pk):
    """
    Edit a product owned by the logged-in vendor.
    """
    product = get_object_or_404(
        Product,
        pk=pk,
        store__owner=request.user,
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            instance=product,
            user=request.user,
        )

        if form.is_valid():

            form.save()

            return redirect("product_list")

    else:

        form = ProductForm(
            instance=product,
            user=request.user,
        )

    return render(
        request,
        "store/product_form.html",
        {
            "form": form,
            "title": "Edit Product",
        },
    )


@login_required
def product_delete(request, pk):
    """
    Delete a product owned by the logged-in vendor.
    """
    product = get_object_or_404(
        Product,
        pk=pk,
        store__owner=request.user,
    )

    if request.method == "POST":

        product.delete()

        return redirect("product_list")

    return render(
        request,
        "store/product_delete.html",
        {
            "product": product,
        },
    )
    
@login_required
def checkout(request):
    """
    Complete the checkout process.
    """
    cart = Cart(request)

    products = cart.products()

    if not products:
        return redirect("cart")

    total = Decimal("0.00")

    order = Order.objects.create(
        buyer=request.user,
        total=0,
    )

    for product in products:

        quantity = cart.quantities()[str(product.id)]

        subtotal = product.price * quantity

        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price,
        )

    order.total = total
    order.save()

    cart.clear()

    send_mail(
        subject=f"Invoice #{order.id}",
        message=(
            f"Thank you for your purchase!\n\n"
            f"Order Number: {order.id}\n"
            f"Total: R{total}"
        ),
        from_email=None,
        recipient_list=[request.user.email],
        fail_silently=True,
    )

    return render(
        request,
        "store/invoice.html",
        {
            "order": order,
        },
    )
    
@login_required
def add_review(request, pk):
    """
    Add a review for a product.
    """

    product = get_object_or_404(
        Product,
        pk=pk,
    )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            review = form.save(commit=False)

            review.product = product

            review.buyer = request.user

            review.verified = OrderItem.objects.filter(
                order__buyer=request.user,
                product=product,
            ).exists()

            review.save()

            return redirect(
                "product_detail",
                pk=product.pk,
            )

    else:

        form = ReviewForm()

    return render(
        request,
        "store/review_form.html",
        {
            "form": form,
            "product": product,
        },
    )
