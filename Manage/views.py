from datetime import date
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Shop.models import Order, Dish, Cart, Customer

# Create your views here.


def Home_page(request):
    queryset = Dish.objects.filter()
    return render(request, 'index.html', {'Dish': queryset})


def updatecart(request):
    data = json.loads(request.body)
    id = data['id']
    action = data['action']
    user = request.user
    customer = Customer.objects.get(customer_id=user.id)
    cart, created = Cart.objects.get_or_create(customer_id=customer.id)
    print(Customer.id)
    if action == 'add':
        order, created = Order.objects.get_or_create(
            cart_id=cart.id, dish_id=id)
        order.amount += 1
        order.save()
    else:
        order, created = Order.objects.get_or_create(
            cart_id=cart.id, dish_id=id)
        order.amount -= 1
        if order.amount < 0:
            order.delete()
        order.save()
    return JsonResponse('added', safe=False)


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


def GetAllDish(request):
    queryset = Dish.objects.filter()
    return render(request, 'index.html', {'Dish': queryset})


# def GetAllType_of_DishInMenu(request):
#     queryset = Type_of_Dish.objects.filter()
#     return render(request, 'Test.html', {'AllTypeofdish': queryset})
