from django.contrib.auth import authenticate , login
from django.shortcuts import render , redirect
from django.views import View
from .forms import LoginForm

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["email"], password=cd["password"])
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("email", "Invalid user data")
        else:
            form.add_error("email", "Invalid data")
    else:
        form = LoginForm()

    return render(request, "account/login.html", {"form": form})