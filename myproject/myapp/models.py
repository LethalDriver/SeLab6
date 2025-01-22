from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.


def validate_price(value):
    if value <= 0:
        raise ValidationError("Price must be greater than 0")


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[validate_price]
    )
    available = models.BooleanField()


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)


class Order(models.Model):
    STATUS_CHOICES = [
        ("NEW", "New"),
        ("PROCESSING", "In Process"),
        ("SENT", "Sent"),
        ("COMPLETED", "Completed"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")

    def calculate_total_price(self):
        total_price = sum(product.price for product in self.products.all())
        return total_price

    def can_be_fulfilled(self):
        return all(product.available for product in self.products.all())
