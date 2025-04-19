from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('login/', views.login_user, name='user_login'),
    path("register/", views.register_user, name="user_register"),
    path("logout/", views.logout_user, name="user_logout"),
    path("add/address/", views.add_address, name="add_address"),

    # Add the path for the user dashboard
    path("dashboard-user/", views.user_dashboard, name="user_dashboard"),  # New path for user dashboard

    # Add the path for the seller dashboard if the user is a seller
    path("dashboard-seller/", views.seller_dashboard, name="seller_dashboard"),  # New path for seller dashboard
]
