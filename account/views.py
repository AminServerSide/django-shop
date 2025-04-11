from django.contrib.auth import authenticate , login
from django.shortcuts import render , redirect
from django.views import View
from .forms import LoginForm
from .models import User

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.get(email=cd["email"])  # Retrieve user by email
            login(request, user)
            return redirect("/")
        else:
            form.add_error("email", "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})