from django.test import TestCase
from decimal import Decimal
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product(name='Temporary product', price=Decimal('1.99'), available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, Decimal('1.99'))
        self.assertTrue(temp_product.available)
        
    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='Temporary product', price=Decimal('-1.99'), available=True)
            temp_product.full_clean()
            
    def test_create_product_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(price=Decimal('1.99'), available=True)
            temp_product.full_clean() 

    def test_create_product_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product(name='', price=Decimal('1.99'), available=True)
            temp_product.full_clean()

    def test_create_product_edge_name_length(self):
        valid_name = 'a' * 255
        temp_product = Product.objects.create(name=valid_name, price=Decimal('1.99'), available=True)
        self.assertEqual(temp_product.name, valid_name)
        
    def test_create_product_invalid_name_length(self):
        invalid_name = 'a' * 256 
        with self.assertRaises(ValidationError):
            temp_product = Product(name=invalid_name, price=Decimal('1.99'), available=True)
            temp_product.full_clean()
            
    def test_create_product_with_minimum_price(self):
        temp_product = Product(name='Minimum Price', price=Decimal('0.01'), available=True)
        self.assertEqual(temp_product.price, Decimal('0.01'))

    def test_create_product_with_maximum_price(self):
        temp_product = Product(name='Maximum Price', price=Decimal('9999999.99'), available=True)
        self.assertEqual(temp_product.price, Decimal('9999999.99'))      

    def test_create_product_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid Price', price=Decimal('1.999'), available=True)
            temp_product.full_clean()
            
class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='John Doe', address='123 Main St')
        self.assertEqual(temp_customer.name, 'John Doe')
        self.assertEqual(temp_customer.address, '123 Main St')

    def test_create_customer_missing_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='John Doe')
            temp_customer.full_clean()

    def test_create_customer_blank_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='', address='123 Main St')
            temp_customer.full_clean()

    def test_create_customer_edge_name_length(self):
        valid_name = 'a' * 100
        temp_customer = Customer.objects.create(name=valid_name, address='123 Main St')
        self.assertEqual(temp_customer.name, valid_name)
        
    def test_create_customer_invalid_name_length(self):
        invalid_name = 'a' * 101
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name=invalid_name, address='123 Main St')
            temp_customer.full_clean()

    def test_create_customer_edge_address_length(self):
        valid_address = 'a' * 255
        temp_customer = Customer.objects.create(name='John Doe', address=valid_address)
        self.assertEqual(temp_customer.address, valid_address)
        
    def test_create_customer_invalid_address_length(self):
        invalid_address = 'a' * 256
        with self.assertRaises(ValidationError):
            temp_customer = Customer(name='John Doe', address=invalid_address)
            temp_customer.full_clean()
            
class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='John Doe', address='123 Main St')
        self.product1 = Product.objects.create(name='Product 1', price=Decimal('10.00'), available=True)
        self.product2 = Product.objects.create(name='Product 2', price=Decimal('20.00'), available=False)
        self.product3 = Product.objects.create(name='Product 3', price=Decimal('30.00'), available=True)

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status='NEW')
        order.products.set([self.product1, self.product3])
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'NEW')
        self.assertEqual(order.products.count(), 2)

    def test_create_order_missing_customer(self):
        with self.assertRaises(ValidationError):
            order = Order(status='NEW')
            order.full_clean()

    def test_create_order_invalid_status(self):
        with self.assertRaises(ValidationError):
            order = Order(customer=self.customer, status='INVALID')
            order.full_clean()

    def test_calculate_total_price_with_products(self):
        order = Order.objects.create(customer=self.customer, status='NEW')
        order.products.set([self.product1, self.product3])
        self.assertEqual(order.calculate_total_price(), Decimal('40.00'))

    def test_calculate_total_price_no_products(self):
        order = Order.objects.create(customer=self.customer, status='NEW')
        self.assertEqual(order.calculate_total_price(), Decimal('0.00'))

    def test_order_can_be_fulfilled_all_products_available(self):
        order = Order.objects.create(customer=self.customer, status='NEW')
        order.products.set([self.product1, self.product3])
        self.assertTrue(order.can_be_fulfilled())

    def test_order_can_be_fulfilled_some_products_unavailable(self):
        order = Order.objects.create(customer=self.customer, status='NEW')
        order.products.set([self.product1, self.product2])
        self.assertFalse(order.can_be_fulfilled())