from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_POST

from cart.cart_modules import Cart
from cart.models import Order, OrderItem
from .forms import LoginForm, UserCreationForm , AddressCreationForm
from .models import User


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(email=cd["email"])  # Retrieve user by email
            login(request, user)
            next_page = request.GET.get("next")
            if next_page:
                return redirect(next_page)
            return redirect("/")
        else:
            form.add_error("email", "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            messages.success(request, "Registration successful! Welcome!")
            return redirect("/")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, "account/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("/")



def add_address(request):
    if request.method == "POST":
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
    else:
        form = AddressCreationForm()

    return render(request, "account/add_address.html", {"form": form})












