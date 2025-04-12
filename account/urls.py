from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
    path('login/', views.login_user, name='user_login'),
    path("register/", views.register_user, name="user_register"),
    path("logout/", views.logout_user, name="user_logout"),
]