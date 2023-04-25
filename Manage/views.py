from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

# Create your views here.


def Home_page(request):

    return render(request, 'index.html')


def cart(request):
    return render(request, 'cart.html')


def contact(request):
    return render(request, 'contact.html')


def menu(request):
    return render(request, 'menu.html')


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def about(request):
    return render(request, 'about.html')


# def GetAllProductInMenu(request):
#     queryset = Menu.objects.filter()
#     return render(request, 'Test.html', {'Allproduct': queryset})


# def GetAllType_of_DishInMenu(request):
#     queryset = Type_of_Dish.objects.filter()
#     return render(request, 'Test.html', {'AllTypeofdish': queryset})
