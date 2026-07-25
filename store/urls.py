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
        "cart/add/<int:pk>/",
        views.add_to_cart,
        name="add_to_cart",
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
        "product/<int:pk>/review/",
        views.add_review,
        name="add_review",
),
]
