from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/', views.product_detail_view, name='product-detail'),
    path('navbar' , views.navbar_partial , name='navbar'),
]