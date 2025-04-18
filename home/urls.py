from django.urls import path
from . import views
from .views import HomeView
from django.views.decorators.cache import cache_page

from django.views.decorators.cache import cache_page


app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view() , name='home'),
]
