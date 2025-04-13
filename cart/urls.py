from django.urls import path
from . import  views

app_name = "cart"

urlpatterns = [
    path('detail' , views.cart_detail_view, name='cart_detail'),
    path('add<int:pk>' , views.cart_add_view, name='cart_add'),
]