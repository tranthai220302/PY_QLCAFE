from datetime import date
from django.contrib.auth import authenticate, login, logout, decorators
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Shop.models import Order, Dish, Cart, Customer

# Create your views here.


def Home_page(request):
    queryset = Dish.objects.filter()
    if not request.user.is_authenticated:
        return render(request, 'index.html', {'Dish': queryset})
    else:
        user = request.user
        if user.is_staff == True:
            return render(request, 'index.html', {'Dish': queryset})
        else:
            return render(request, 'formLogin.html')


def formlogin(request):
    return render(request, 'formLogin.html')


def my_login(request):
    if request.method == "POST":
        queryset = Dish.objects.filter()
        if not request.user.is_authenticated:
            user_name = request.POST.get('user')
            pass_word = request.POST.get('pass')
            my_user = authenticate(
                request, username=user_name, password=pass_word)
            print(user_name)
            print(pass_word)
            if my_user is None:
                print("dfdfd")
                return render(request, 'formLogin.html')
            login(request, my_user)
            return render(request, 'index.html', {'Dish': queryset})
        return render(request, 'index.html', {'Dish': queryset})


def my_logout(request):
    logout(request)
    queryset = Dish.objects.filter()
    return render(request, 'index.html', {'Dish': queryset})


def updatecart(request):
    data = json.loads(request.body)
    id = data['id']
    action = data['action']
    user = request.user
    customer = Customer.objects.get(customer_id=user.id)
    cart, created = Cart.objects.get_or_create(customer_id=customer.id)
    order, created = Order.objects.get_or_create(
        cart_id=cart.id, dish_id=id)
    if action == 'add':
        order.amount += 1
        order.save()
    else:
        order.amount -= 1
        if order.amount == -1:
            order.amount = 0
        order.save()
    orders = Order.objects.filter(cart_id=cart.id)
    total = 0
    for oder in orders:
        total += oder.dish.price * oder.amount
    data = {'cart': total, 'amount': order.amount}
    json_data = json.dumps(data)
    return JsonResponse(json_data, safe=False)


@decorators.login_required(login_url='/formlogin')
def cart(request):

    user = request.user
    customer = Customer.objects.get(customer_id=user.id)
    zero_objects = Order.objects.filter(amount=0)

    zero_objects.delete()
    cart, created = Cart.objects.get_or_create(customer_id=customer.id)
    order = Order.objects.filter(cart_id=cart.id)
    total = 0
    for oder in order:
        total += oder.dish.price * oder.amount
    return render(request, 'cart.html', {'orders': order, 'total': total})


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
