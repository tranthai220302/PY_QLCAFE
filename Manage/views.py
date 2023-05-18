from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, decorators
import json
from django.http import HttpResponse, JsonResponse
from Shop.models import Order, Dish, Cart, Customer, Menu, Employee
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import math
import random
from django.views.decorators.csrf import csrf_exempt
import os
import shutil
from django.conf import settings
from Shop.models import User
# Create your views here.


def Home_page(request):
    queryset = Dish.objects.filter()
    nhanvien = Employee.objects.filter()
    if not request.user.is_authenticated:
        return render(request, 'Customer/index.html', {'Dish': queryset, 'nhanvien': nhanvien})
    else:
        user = request.user
        if user.is_staff == True:
            return render(request, 'Customer/index.html', {'Dish': queryset, 'nhanvien': nhanvien})
        else:
            if user.is_admin == True:
                listCustomer = Customer.objects.filter()
                return render(request, 'Admin/manageEmployee.html', {'Dish': queryset, 'nhanvien': nhanvien, 'list_Customer': listCustomer})
            else:
                list_menu = Menu.objects.filter()
                nhanvien = Employee.objects.filter(employee_id=user.id)
                return render(request, 'Manage/home.html', {'list_menu': list_menu, 'my_user': user, 'nhanvien': nhanvien})


@decorators.login_required(login_url='/formlogin')
def myaccount(request):
    return render(request, 'Customer/myaccount.html')


def myaccountNV(request):
    return render(request, 'Manage/myaccount.html')


def formlogin(request):
    return render(request, 'Customer/formLogin.html')


def my_login(request):
    if request.method == "POST":
        queryset = Dish.objects.filter()
        user = request.user
        list_menu = Menu.objects.filter()
        nhanvien = Employee.objects.filter()
        if not user.is_authenticated:
            user_name = request.POST.get('username')
            pass_word = request.POST.get('password')
            print(user_name)
            print(pass_word)
            my_user = authenticate(
                request, username=user_name, password=pass_word)
            if my_user is None:
                return render(request, 'Customer/formLogin.html')
            login(request, my_user)
            print(my_user.is_staff)
            if my_user.is_staff == True:
                return HttpResponseRedirect('/', {'Dish': queryset, 'nhanvien': nhanvien})
            else:
                if my_user.is_admin == True:
                    listCustomer = Customer.objects.filter()
                    return HttpResponseRedirect('manage_Employee', {'Dish': queryset, 'nhanvien': nhanvien, 'list_Customer': listCustomer})
                else:
                    return HttpResponseRedirect('home', {'list_menu': list_menu, 'my_user': user, 'nhanvien': nhanvien})
        else:
            if my_user.is_staff == True:
                return HttpResponseRedirect('/', {'Dish': queryset, 'nhanvien': nhanvien})
            else:
                if my_user.is_admin == True:
                    listCustomer = Customer.objects.filter()
                    return HttpResponseRedirect('manage_Employee', {'Dish': queryset, 'nhanvien': nhanvien, 'list_Customer': listCustomer})
                else:
                    return HttpResponseRedirect('home', {'list_menu': list_menu, 'my_user': user, 'nhanvien': nhanvien})
    else:
        user = request.user
        list_menu = Menu.objects.filter()
        nhanvien = Employee.objects.filter(employee_id=user.id)
        if not user.is_authenticated:
            return render(request, 'Customer/formLogin.html')
        else:
            if my_user.is_staff == True:
                return HttpResponseRedirect('/', {'Dish': queryset, 'nhanvien': nhanvien})
            else:
                if my_user.is_admin == True:
                    listCustomer = Customer.objects.filter()
                    return HttpResponseRedirect('manage_Employee', {'Dish': queryset, 'nhanvien': nhanvien, 'list_Customer': listCustomer})
                else:
                    return HttpResponseRedirect('home', {'list_menu': list_menu, 'my_user': user, 'nhanvien': nhanvien})


@decorators.login_required(login_url='/formlogin')
def my_logout(request):
    logout(request)
    queryset = Dish.objects.filter()
    nhanvien = Employee.objects.filter()
    return HttpResponseRedirect('/')


@ decorators.login_required(login_url='/formlogin')
def purchaseorder(request):
    user = request.user
    customer, created = Customer.objects.get_or_create(customer_id=user.id)
    carts = customer.cart_set.all().prefetch_related('order_set__dish')
    carts = reversed(carts)
    return render(request, 'Customer/purchaseorder.html', {'customer': customer, 'carts': carts})


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
            return render(request, 'Customer/formlogin.html', {"form": "form1"})
        User.objects.create_superuser(
            username=_username, email=email, password=password, first_name=firstname, last_name=lastname)
        user = authenticate(request, username=_username, password=password)
        login(request, user)
        Customer.objects.create(
            customer=user, address=_address, number_phone=phone)
        queryset = Dish.objects.filter()
        return HttpResponseRedirect('/', {'Dish': queryset})
    else:
        return HttpResponseRedirect('/')


def signupemployee(request, id=0):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        _username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        _address = request.POST.get('Address')
        phone = request.POST.get('phone')
        posi = request.POST.get('position')
        image = request.POST.get('image')
        my_user = User.objects.filter(username=_username)
        if my_user.exists():
            print('You already have')
            nhanvien = Employee.objects.filter()
            listCustomer = Customer.objects.filter()
            return HttpResponseRedirect('manage_Employee')
        if id == 0:
            User.objects.create_user(
                username=_username, email=email, password=password, first_name=firstname, last_name=lastname, is_staff=False)
            user = authenticate(request, username=_username, password=password)
            print(user)
            Employee.objects.create(
                employee=user, address=_address, number_phone=phone, position=posi, image="img/"+image)

            nhanvien = Employee.objects.filter()
            return HttpResponseRedirect('manage_Employee', {'nhanvien': nhanvien})
        else:
            employee = Employee.objects.get(id=id)
            employee.address = _address
            employee.number_phone = phone
            employee.position = posi
            employee.employee.email = email
            employee.employee.first_name = firstname
            employee.employee.last_name = lastname
            employee.employee.save()
            employee.save()
            nhanvien = Employee.objects.filter()
            return HttpResponseRedirect('manage_Employee', {'nhanvien': nhanvien})

    else:
        print('You already have123')
        nhanvien = Employee.objects.filter()
        return render(request, 'Admin/manageEmployee.html', {'nhanvien': nhanvien})


def delete(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    nhanvien = Employee.objects.filter()
    return render(request, 'Admin/manageEmployee.html', {'nhanvien': nhanvien})


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
    return render(request, 'Customer/cart.html', {'orders': order, 'total': total})


@decorators.login_required(login_url='/formlogin')
def pay(request):
    user = request.user
    customer, created = Customer.objects.get_or_create(customer_id=user.id)
    zero_objects = Order.objects.filter(amount=0)

    zero_objects.delete()
    cart, created = Cart.objects.get_or_create(
        customer_id=customer.id, status='ordering')
    print("1ewewe")
    if cart.total > 0:
        print(1)
        cart.status = 'delivery'
        cart.save()
        return render(request, 'Customer/cart.html')
    return render(request, 'Customer/cart.html')


def contact(request):
    return render(request, 'Customer/contact.html')


def manage_Employee(request):
    nhanvien = Employee.objects.filter()
    return render(request, 'Admin/manageEmployee.html', {'nhanvien': nhanvien})


def menu(request):
    queryset = Dish.objects.filter()
    return render(request, 'Customer/menu.html', {'Dish': queryset})


def service(request):
    return render(request, 'Customer/service.html')


def team(request):
    nhanvien = Employee.objects.filter()
    return render(request, 'Customer/team.html', {'nhanvien': nhanvien})


def testimonial(request):
    return render(request, 'Customer/testimonial.html')


def about(request):
    return render(request, 'Customer/about.html')


def home(request):
    user = request.user
    my_user = User.objects.get(id=user.id)
    nhanvien = Employee.objects.get(employee_id=user.id)
    nhanvien = Employee.objects.get(employee_id=user.id)
    list_menu = Menu.objects.filter()
    return render(request, 'Manage/home.html', {'list_menu': list_menu, 'my_user': my_user, 'nhanvien': nhanvien})


def manage_menu(request, id, id_page):
    user = request.user
    my_user = User.objects.get(id=user.id)
    nhanvien = Employee.objects.get(employee_id=user.id)
    print(id)
    list_Dish = Dish.objects.filter(menu_id=id).order_by('-id')
    num_page = math.ceil(list_Dish.count()/6)
    arr = [i+1 for i in range(num_page)]
    paginator = Paginator(list_Dish, 6)  # phân trang với 5 items/trang
    try:
        list_Dish = paginator.page(id_page)
    except PageNotAnInteger:
        list_Dish = paginator.page(1)
    except EmptyPage:
        list_Dish = paginator.page(paginator.num_pages)
    menu = Menu.objects.get(id=id)
    return render(request, 'Manage/add.html', {'list_Dish': list_Dish, 'menu': menu, 'num_page': arr, 'id_page': id_page, 'my_user': my_user, 'nhanvien': nhanvien})


@csrf_exempt
def delete_post(request):

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        Dish_delete = Dish.objects.get(id=post_id)
        Dish_delete.delete()
        data = {'deleted': True}
    else:
        data = {'deleted': False}
    return JsonResponse(data)


@csrf_exempt
def create_dish(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES['image']
        menu_id = request.POST['menu_id']
        # Lưu tập tin vào thư mục "static/media/images"
        image_name = os.path.join(
            settings.MEDIA_ROOT, 'media', request.FILES['image'].name)
        with open(image_name, 'wb') as f:
            f.write(request.FILES['image'].read())
        dish = Dish(menu_id=menu_id, name=name, price=price,
                    image='media/' + request.FILES['image'].name)
        dish.save()
        image_url = 'media/' + request.FILES['image'].name
        url = "{% static '"+image_url+"' %}"

        return JsonResponse(
            {
                'success':  True,
                'id': dish.id,
                'image_url':  image_url,
                'name': dish.name,
                'price': dish.price
            }
        )
    else:
        return HttpResponse('Request method is not POST.')


@csrf_exempt
def edit_dish(request):
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        name = request.POST['name']
        price = request.POST['price']
        # Lưu tập tin vào thư mục "static/media/images"
        image_name = os.path.join(
            settings.MEDIA_ROOT, 'media', request.FILES['image'].name)
        with open(image_name, 'wb') as f:
            f.write(request.FILES['image'].read())
        dish = Dish.objects.get(id=dish_id)
        dish.name = name
        dish.price = price
        dish.image = 'media/' + request.FILES['image'].name
        dish.save()
        return JsonResponse({'success':  True})
    return HttpResponse('Request method is not POST.')


# Manage Customer

def manage_Customer(request, id_page):
    user = request.user
    my_user = User.objects.get(id=user.id)
    list_Customer = Customer.objects.filter()
    num_page = math.ceil(list_Customer.count()/4)
    arr = [i+1 for i in range(num_page)]
    paginator = Paginator(list_Customer, 4)  # phân trang với 5 items/trang
    try:
        list_Customer = paginator.page(id_page)
    except PageNotAnInteger:
        list_Customer = paginator.page(1)
    except EmptyPage:
        list_Customer = paginator.page(paginator.num_pages)
    return render(request, 'Admin/manageCutomer.html', {'list_Customer': list_Customer, 'num_page': arr, 'id_page': id_page})


def delete_customer(request, id, id_page):
    user = request.user

    customer_delete = Customer.objects.get(id=id)
    customer_delete.delete()
    list_Customer = Customer.objects.filter()
    num_page = math.ceil(list_Customer.count()/4)
    arr = [i+1 for i in range(num_page)]
    paginator = Paginator(list_Customer, 4)  # phân trang với 5 items/trang
    try:
        list_Customer = paginator.page(id_page)
    except PageNotAnInteger:
        list_Customer = paginator.page(1)
    except EmptyPage:
        list_Customer = paginator.page(paginator.num_pages)
    return render(request, 'Admin/manageCutomer.html', {'list_Customer': list_Customer, 'num_page': arr, 'id_page': id_page})


def success_order(request, id):
    order_update = Cart.objects.get(id=id)
    order_update.status = 'receiced'
    order_update.save()
    listOrder = Cart.objects.filter(status='delivery')
    return render(request, 'Manage/cartnhanvien.html', {'listOrder': listOrder})


def listOrder(request):
    listOrder = Cart.objects.filter(status='delivery')
    return render(request, 'Manage/cartnhanvien.html', {'listOrder': listOrder})
