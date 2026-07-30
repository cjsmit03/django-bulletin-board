# Django eCommerce Application

## Overview

This project is a Django-based eCommerce web application developed as part of the HyperionDev Introduction to Software Engineering course.

The application allows vendors to create and manage online stores, upload products for sale, and allows customers to browse products, add items to a shopping cart, place orders, and leave reviews for purchased products.

The project also includes:

- User authentication and authorization
- Customer and Vendor roles
- Store and product management
- Shopping cart and checkout
- Order history
- Product reviews
- REST API endpoints using Django REST Framework
- Reddit API integration using the requests library

---

## Features

### Customer

- Register and log in
- Browse stores and products
- Add products to cart
- Checkout orders
- View invoices
- Leave product reviews

### Vendor

- Register and log in
- Create stores
- Manage products
- View customer reviews

### Administrator

- Manage users
- Create product categories
- Manage the application through the Django Admin interface

---

## Requirements

- Python 3.14+
- MySQL Server
- pip
- Virtual Environment

---

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ecommerce_project
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```cmd
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Setup

Create a Maria/MySQL database.

Example:

```sql
CREATE DATABASE ecommerce_db;
```

Update the database credentials inside:

```
ecommerce/settings.py
```

Run the migrations:

```bash
python manage.py migrate
```

Create an administrator:

```bash
python manage.py createsuperuser
```

---

## Running the application

Start the server:

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

Admin:

```
http://127.0.0.1:8000/admin/
```

---

## Initial Setup

Before vendors can create products, an administrator must first create one or more product categories.

Steps:

1. Log in to the Django Admin.
2. Open **Categories**.
3. Create one or more categories (e.g. Electronics, Books, Clothing).
4. Vendors can now create products.

---

## Typical Workflow

1. Register a Vendor account.
2. Log in.
3. Create a Store.
4. Create Products.
5. Register a Customer account.
6. Browse products.
7. Add products to cart.
8. Checkout.
9. Leave reviews for purchased products.

---

## REST API

Available endpoints:

```
GET    /api/vendors/<vendor_id>/stores/
GET    /api/stores/<store_id>/products/
GET    /api/products/<product_id>/reviews/

POST   /api/stores/create/
POST   /api/products/create/
```

---

## Reddit Integration

Visit:

```
/reddit/
```

The application retrieves posts from the **r/django** subreddit using the Reddit API.

> **Note:** Reddit may return HTTP 403 for anonymous requests depending on Reddit's current API restrictions and network policies.

---

## Author

CJ Smit

Introduction to Software Engineering

HyperionDev
