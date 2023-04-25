from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home_page, name="Home_page"),
    path('about', views.about, name="about"),
    path('cart', views.cart, name="cart"),
    path('contact', views.contact, name="contact"),
    path('menu', views.menu, name="menu"),
    path('service', views.service, name="service"),
    path('team', views.team, name="team"),
    path('testimonial', views.testimonial, name="testimonial"),
]
