from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('detail', views.cart_detail_view, name='cart_detail'),
    path('add/<int:pk>', views.cart_add_view, name='cart_add'),
    path('remove/<str:pk>', views.cart_remove_view, name='cart_remove'),
    path('order/<int:id>', views.order_detail, name='order_detail'),
    path('order/create', views.order_creation, name='order_creation'),
    path('applydiscount/<int:pk>', views.ApplyDiscountView.as_view(), name='apply_discount'),
    path('payment/<int:pk>/', views.fake_payment_view, name='fake_payment'),
    path('verify/', views.fake_verify_view, name='fake_verify'),
    path('pay/<int:pk>/', views.payment_view, name='payment'),  # New URL for payment view

]
