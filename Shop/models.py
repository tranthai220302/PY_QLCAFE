
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)


class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    number_phone = models.TextField(max_length=10)
    username = User.username
    password = User.password
    image = models.FileField(blank=True, null=True,
                             upload_to='images/', default='img/avata.jpg')

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name


class Employee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    number_phone = models.TextField(max_length=10)
    username = User.username
    password = User.password
    option1 = 'Phục Vụ'
    option2 = 'Bưng Bê'
    option3 = 'Pha Bhế'
    TYPE = (
        (option1, option1),
        (option2, option2),
        (option3, option3),
    )
    position = models.CharField(max_length=50, choices=TYPE, default=option1)
    image = models.FileField(blank=True, null=True,
                             upload_to='images/', default='img/avata.jpg')
    name = str(User.first_name) + " " + str(User.last_name)

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name

    def delete(self, *args, **kwargs):
        self.employee.delete()
        super().delete(*args, **kwargs)


class Menu(models.Model):
    # disk = models.ForeignKey(Disk, on_delete=models.CASCADE)

    Coffee = 'Coffee'
    Milk_Tea = 'Milk_Tea'
    CaKe = 'Cake'
    TYPE = (
        (Coffee, Coffee),
        (Milk_Tea, Milk_Tea),
        (CaKe, CaKe),
    )
    type = models.CharField(max_length=50, choices=TYPE)
    details = models.CharField(max_length=200)
    image = models.FileField(blank=True, null=True, upload_to='images/')

    def __str__(self):
        return self.type


class Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.IntegerField()
    image = models.FileField(blank=True, null=True,
                             upload_to='media/')

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    ordering = 'ordering'
    delivery = 'delivery'
    received = 'received'
    Status = (
        (ordering, ordering),
        (delivery, delivery),
        (received, received)
    )
    status = models.CharField(max_length=50, choices=Status, default=ordering)

    def __str__(self):
        return self.customer.__str__() + " " + self.date.__str__()


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    details = models.CharField(max_length=100, default="")
