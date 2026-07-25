# Django eCommerce Application

## Overview

This project is a simple eCommerce web application developed using Django as part of the HyperionDev Introduction to Software Engineering course.

The application allows users to register as either Vendors or Customers. Vendors can manage stores and products, while Customers can browse products, add them to a shopping cart, complete checkout, and leave product reviews.

---

## Features

### User Management

- User registration
- User login/logout
- Vendor and Customer roles
- Password reset

### Vendor Features

- Create stores
- View stores
- Edit stores
- Delete stores
- Create products
- View products
- Edit products
- Delete products

### Customer Features

- Browse products
- View product details
- Add products to cart
- Session-based shopping cart
- Checkout
- Invoice generation
- Product reviews
- Verified and unverified reviews

### Other Features

- Django authentication
- Django Groups and Permissions
- Bootstrap 5 interface
- Django Admin
- Unit tests

---

## Technologies Used

- Python 3
- Django 6
- Bootstrap 5
- SQLite (development database)

---

## Installation

Clone the repository.

```bash
git clone <repository-url>
cd ecommerce_project
```

Create a virtual environment.

```bash
python3 -m venv venv
```

Activate the virtual environment.

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Run database migrations.

```bash
python3 manage.py migrate
```

Create an administrator account.

```bash
python3 manage.py createsuperuser
```

Run the development server.

```bash
python3 manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Running Tests

Run all unit tests.

```bash
python3 manage.py test
```

---

## Project Structure

```
ecommerce_project/

accounts/
store/
ecommerce/
templates/
static/
Planning/

manage.py
requirements.txt
README.md
```

---

## Planning

The Planning folder contains:

- requirements.md
- ui_design.md
- security.md
- failure_recovery.md

---

## Author

CJ Smit

HyperionDev – Introduction to Software Engineering
