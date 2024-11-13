from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Delete existing data
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        for i in range(1, 5):
            products = []
            for j in range(1, 4):  
                product = Product.objects.create(
                    name=f"Sample Product {j*i}",
                    price=19.99 + j*i,  # Example to vary the price
                    available=True,
                )
                products.append(product)

            customer = Customer.objects.create(
                name=f"Customer {i}", address=f"Sample Street {i*11}"
            )
            order = Order.objects.create(customer=customer, status="NEW")
            for product in products:
                order.products.add(product)

        self.stdout.write(self.style.SUCCESS("Data created successfully."))
