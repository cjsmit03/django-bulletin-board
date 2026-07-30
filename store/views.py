"""
Views for the Store application.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .cart import Cart
from .models import Product, Store, Review
from decimal import Decimal
from .forms import ProductForm, ReviewForm, StoreForm, CategoryForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer

from django.core.mail import send_mail

from .models import Order, OrderItem

from .functions.reddit import get_reddit_posts
def home(request):
    """
    Display the home page and all available products.
    """
    products = Product.objects.all()

    return render(
        request,
        "store/home.html",
        {
            "products": products,
        },
    )


def product_detail(request, pk):
    """
    Display detailed information about a product.
    """
    product = get_object_or_404(Product, pk=pk)

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
        },
    )


def add_to_cart(request, pk):
    """
    Add a product to the shopping cart.
    """
    cart = Cart(request)
    cart.add(pk)
    return redirect("cart")


def remove_from_cart(request, pk):
    """
    Remove a product from the shopping cart.
    """
    cart = Cart(request)
    cart.remove(pk)
    return redirect("cart")


def cart_view(request):
    """
    Display the contents of the shopping cart.
    """
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
    """
    Display all stores belonging to the logged-in vendor.
    """

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
    """
    Create a new store.
    """

    if not request.user.groups.filter(name="Vendor").exists():
        return redirect("home")

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
    """
    Update an existing store.
    """

    if not request.user.groups.filter(name="Vendor").exists():
        return redirect("home")

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
    """
    Delete an existing store.
    """

    if not request.user.groups.filter(name="Vendor").exists():
        return redirect("home")

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

    if not request.user.groups.filter(name="Vendor").exists():
        return redirect("home")

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
def category_create(request):
    """
    Create a category.
    """

    if not request.user.groups.filter(name="Vendor").exists():
        return redirect("home")

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = CategoryForm()

    return render(
        request,
        "store/category_form.html",
        {"form": form},
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

@api_view(['GET'])
def api_vendor_stores(request, vendor_id):
    """
    Return all stores belonging to the specified vendor.
    """
    stores = Store.objects.filter(owner_id=vendor_id)
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_store_products(request, store_id):
    """
    Return all products belonging to the specified store.
    """
    products = Product.objects.filter(store_id=store_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_product_reviews(request, product_id):
    """
    Return all reviews for the specified product.
    """
    reviews = Review.objects.filter(product_id=product_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_create_store(request):
    """
    Create a new store for an authenticated vendor.
    """
    if not request.user.groups.filter(name="Vendor").exists():
        return Response(
            {"error": "Only vendors can create stores."},
            status=403,
        )

    serializer = StoreSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_create_product(request):
    """
    Create a new product for an authenticated vendor.
    """ 
    store_id = request.data.get("store")

    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response(
            {"error": "Store not found."},
            status=404,
        )

    if store.owner != request.user:
        return Response(
            {"error": "You can only add products to your own store."},
            status=403,
        )

    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

def reddit_feed(request):
    """
    Display the latest posts from the configured Reddit subreddit.
    """
    posts = get_reddit_posts("django")

    context = {
        "posts": posts
    }

    return render(request, "store/reddit_feed.html", context)
