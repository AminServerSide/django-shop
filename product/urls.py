from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/', views.product_detail_view, name='product-detail'),
    path('navbar' , views.navbar_partial , name='navbar'),
    path('category' , views.category_list , name='category'),
    path('all' , views.product_list , name='products_list'),
    path('<int:product_id>/comment/create/', views.create_comment, name='create_comment'),

]