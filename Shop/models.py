

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    number_phone = models.TextField(max_length=10)
    username = User.username
    password = User.password

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name


class Employee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    number_phone = models.TextField(max_length=10)
    username = User.username
    password = User.password
    name = str(User.first_name) + " " + str(User.last_name)

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name


class Menu(models.Model):
    # disk = models.ForeignKey(Disk, on_delete=models.CASCADE)

    food = 'Foods'
    drink = 'Drinks'
    refreshment = 'Refreshments'
    sale_off_dish = 'Sale off Dishes'
    TYPE = (
        (food, food),
        (drink, drink),
        (refreshment, refreshment),
        (sale_off_dish, sale_off_dish)
    )
    type = models.CharField(max_length=50, choices=TYPE)
    details = models.CharField(max_length=200)
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.type


class Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    disabled = 'Disabled'
    enabled = 'Enabled'

    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )

    name = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=STATUS)
    price = models.FloatField()
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    pending = 'Pending'
    completed = 'Completed'
    STATUS = (
        (pending, pending),
        (completed, completed),
    )
    pickup = 'PickUp'
    delivery = 'Delivery'

    TYPE = (
        (pickup, pickup),
        (delivery, delivery),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS)
    type = models.CharField(max_length=100, choices=TYPE)

    def __str__(self):
        return self.customer.__str__() + " " + self.date.__str__()


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details = models.CharField(max_length=100, default="")
