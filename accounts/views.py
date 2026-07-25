"""
Views for user authentication.
"""

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register_user(request):
    """
    Register a new user and assign them to the selected group.
    """
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            role = form.cleaned_data["role"]

            group, created = Group.objects.get_or_create(name=role)

            user.groups.add(group)

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form,
        },
    )


def login_user(request):
    """
    Log a user into the application.
    """
    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():

            login(
                request,
                form.get_user(),
            )

            return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def logout_user(request):
    """
    Log the current user out.
    """
    logout(request)

    return redirect("login")
