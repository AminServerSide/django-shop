from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('contact-us/', views.contact_us, name='contact_us'),
     path('about/', views.about, name='about'),
     path('help/', views.help, name='help'),
]
