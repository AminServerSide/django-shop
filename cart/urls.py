from django.urls import path
from . import  views

app_name = "cart"

urlpatterns = [
    path('detail' , views.cart_detail_view, name='cart_detail'),
    path('add/<int:pk>' , views.cart_add_view, name='cart_add'),
    path('remove/<str:pk>' , views.cart_remove_view, name='cart_remove'),
    path('order/<int:id>', views.Order_detail, name='order_detail'),
    path('order/create', views.OrderCreation, name='order_creation'),

]