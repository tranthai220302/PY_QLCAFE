from datetime import date
from pyexpat.errors import messages
from django.contrib.auth import authenticate, login, logout, decorators
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from Shop.models import Order, Dish, Cart, Customer, User

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


@decorators.login_required(login_url='/formlogin')
def myaccount(request):
    return render(request, 'myaccount.html')


def formlogin(request):
    return render(request, 'formLogin.html')


def my_login(request):
    if request.method == "POST":
        queryset = Dish.objects.filter()
        user = request.user
        if not user.is_authenticated:
            user_name = request.POST.get('username')
            pass_word = request.POST.get('password')
            my_user = authenticate(
                request, username=user_name, password=pass_word)
            print(user_name)
            print(pass_word)
            if my_user is None:
                return render(request, 'formLogin.html')
            login(request, my_user)
            print(user.is_staff)
            if user.is_staff == True:
                return render(request, 'index.html', {'Dish': queryset})
            else:
                return render(request, 'formLogin.html')
        return render(request, 'index.html', {'Dish': queryset})


@decorators.login_required(login_url='/formlogin')
def my_logout(request):
    logout(request)
    queryset = Dish.objects.filter()
    return render(request, 'index.html', {'Dish': queryset})


@decorators.login_required(login_url='/formlogin')
def purchaseorder(request):
    user = request.user
    customer, created = Customer.objects.get_or_create(customer_id=user.id)
    carts = customer.cart_set.all().prefetch_related('order_set__dish')
    carts = reversed(carts)
    return render(request, 'purchaseorder.html', {'customer': customer, 'carts': carts})


def signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        _username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        _address = request.POST.get('Address')
        phone = request.POST.get('phone')
        my_user = User.objects.filter(username=_username)
        if my_user.exists():
            return render(request, 'formlogin.html', {"form": "form1"})
        User.objects.create_superuser(
            username=_username, email=email, password=password, first_name=firstname, last_name=lastname)
        user = authenticate(request, username=_username, password=password)
        login(request, user)
        Customer.objects.create(
            customer=user, address=_address, number_phone=phone)
        queryset = Dish.objects.filter()
        return render(request, 'index.html', {"Dish": queryset})
    else:
        return render(request, 'menu.html')


def updatecart(request):
    data = json.loads(request.body)
    id = data['id']
    action = data['action']
    user = request.user
    customer, created = Customer.objects.get_or_create(customer_id=user.id)
    cart, created = Cart.objects.get_or_create(
        customer_id=customer.id, status='ordering')
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
    cart.total = total
    cart.save()
    data = {'cart': total, 'amount': order.amount}
    json_data = json.dumps(data)
    return JsonResponse(json_data, safe=False)


@decorators.login_required(login_url='/formlogin')
def cart(request):

    user = request.user
    customer, created = Customer.objects.get_or_create(customer_id=user.id)
    zero_objects = Order.objects.filter(amount=0)

    zero_objects.delete()
    cart, created = Cart.objects.get_or_create(
        customer_id=customer.id, status='ordering')
    order = Order.objects.filter(cart_id=cart.id)
    total = 0
    for oder in order:
        total += oder.dish.price * oder.amount
    cart.total = total
    cart.save()
    return render(request, 'cart.html', {'orders': order, 'total': total})


@decorators.login_required(login_url='/formlogin')
def pay(request):
    user = request.user
    customer, created = Customer.objects.get_or_create(customer_id=user.id)
    zero_objects = Order.objects.filter(amount=0)

    zero_objects.delete()
    cart, created = Cart.objects.get_or_create(
        customer_id=customer.id, status='ordering')
    if cart.total > 0:
        print(1)
        cart.status = 'delivery'
        cart.save()
        return render(request, 'cart.html')
    return render(request, 'cart.html')


def contact(request):
    return render(request, 'contact.html')


def menu(request):
    queryset = Dish.objects.filter()
    return render(request, 'menu.html', {'Dish': queryset})


def service(request):
    return render(request, 'service.html')


def team(request):
    return render(request, 'team.html')


def testimonial(request):
    return render(request, 'testimonial.html')


def about(request):
    return render(request, 'about.html')
