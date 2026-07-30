"""
URL configuration for the Store application.
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "product/<int:pk>/",
        views.product_detail,
        name="product_detail",
    ),

    path(
        "cart/",
        views.cart_view,
        name="cart",
    ),

    path(
        "reddit/",
        views.reddit_feed,
        name="reddit_feed",
    ),

    path(
        "api/products/create/",
        views.api_create_product,
        name="api_create_product",
    ),

    path(
        "cart/add/<int:pk>/",
        views.add_to_cart,
        name="add_to_cart",
    ),

    path(
        "api/stores/<int:store_id>/products/",
        views.api_store_products,
        name="api_store_products",
    ),
   
    path(
        "api/products/<int:product_id>/reviews/",
        views.api_product_reviews,
        name="api_product_reviews",
    ),

    path(
        "api/stores/create/",
        views.api_create_store,
        name="api_create_store",
    ),

    path(
        "cart/remove/<int:pk>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),

    path(
        "stores/",
        views.store_list,
        name="store_list",
    ),

    path(
        "api/vendors/<int:vendor_id>/stores/",
        views.api_vendor_stores,
        name="api_vendor_stores",
    ),

    path(
        "stores/create/",
        views.store_create,
        name="store_create",
    ),

    path(
        "stores/<int:pk>/edit/",
        views.store_update,
        name="store_update",
    ),
    path(
        "products/",
        views.product_list,
        name="product_list",
    ),

    path(
        "products/create/",
        views.product_create,
        name="product_create",
    ),

    path(
        "products/<int:pk>/edit/",
        views.product_update,
        name="product_update",
    ),

    path(
        "products/<int:pk>/delete/",
        views.product_delete,
        name="product_delete",
    ),
    path(
        "stores/<int:pk>/delete/",
        views.store_delete,
        name="store_delete",
    ),
    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),
        path(
        "categories/create/",
        views.category_create,
        name="category_create",
    ),
    path(
        "product/<int:pk>/review/",
        views.add_review,
        name="add_review",
),
]
