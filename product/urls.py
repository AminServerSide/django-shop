from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>/', views.product_detail_view, name='product-detail'),
    path('search/', views.search_products, name='search_products'),
    path('like_product/<int:product_id>/', views.like_product, name='like_product'),

    path('navbar' , views.navbar_partial , name='navbar'),
    path('category' , views.category_list , name='category'),
    path('all' , views.ProductListView.as_view() , name='products_list'),
    path('<int:product_id>/comment/create/', views.create_comment, name='create_comment'),
    path('like/<int:pk>/', views.like_product, name='like'),

]