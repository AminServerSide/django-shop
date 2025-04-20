from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('login/', views.login_user, name='user_login'),
    path("register/", views.register_user, name="user_register"),
    path("logout/", views.logout_user, name="user_logout"),
    path("add/address/", views.add_address, name="add_address"),

    # User dashboard
    path("dashboard-user/", views.user_dashboard, name="user_dashboard"),

    # Seller dashboard
    path("dashboard-seller/", views.seller_dashboard, name="seller_dashboard"),

    # Wallet management (optional, if you want wallet views in the future)
    path("wallet/", views.wallet_view, name="wallet_view"),  # New path for wallet view (optional)
]
