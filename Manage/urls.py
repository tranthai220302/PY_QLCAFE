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
    path('updatecart', views.updatecart, name="updatecart"),
    path('my_login', views.my_login, name="my_login"),
    path('formlogin', views.formlogin, name="formlogin"),
    path('my_logout', views.my_logout, name="my_logout"),
    path('signup', views.signup, name="signup"),
    path('signupemployee', views.signupemployee, name="signupemployee"),
    path('pay', views.pay, name="pay"),
    path('purchaseorder', views.purchaseorder, name="purchaseorder"),
    path('myaccount', views.myaccount, name="myaccount"),
    path('delete<int:id>',views.delete, name="delete"),











    path('home/', views.home, name='home'),
    path('manage_menu<int:id>/<int:id_page>',
         views.manage_menu, name='manage_menu'),
    path('delete_post', views.delete_post, name='delete_post'),
    path('edit_dish', views.edit_dish, name='edit_dish'),
    path('create_dish', views.create_dish, name='create_dish'),
    # ManageCustomer
    path('manage_Customer<int:id_page>',
         views.manage_Customer, name='manage_Customer'),


    path('delete_customer<int:id>/<int:id_page>',
         views.delete_customer, name='delete_customer'),

    path('success_order<int:id>', views.success_order, name='success_order'),
    path('cartnhanvien', views.listOrder, name='cartnhanvien'),
]
