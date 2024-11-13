from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    available = models.BooleanField()


class Customer(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Order(models.Model):
    customer = models.ForeignKey(Customer)
    products = models.ManyToManyField(Product)
    date = models.DateField()
    status = models.CharField(max_length=255)
