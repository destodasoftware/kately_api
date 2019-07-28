from django.db import models

from products.models import Product
from users.models import Customer
from utils.models import Utility


class Sale(Utility):
    STATUS_NEW = 'new'
    STATUS_UNFULFILLED = 'unfulfilled'
    STATUS_FULFILLED = 'fulfilled'
    STATUS_FINISH = 'finish'
    STATUS_CHOICES = (
        (STATUS_FULFILLED, 'Fulfilled'),
        (STATUS_UNFULFILLED, 'Unfulfilled'),
        (STATUS_FINISH, 'Finish'),
    )

    sale_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_UNFULFILLED)

    def __str__(self):
        return self.sale_number


class CustomerSale(Utility):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return self.customer.name


class CashSale(Utility):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    bill_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    change_amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)

    def __str__(self):
        return self.sale.sale_number


class TaxSale(Utility):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0.0)
    is_percent = models.BooleanField(default=True)

    def __str__(self):
        return self.sale.sale_number


class Shipping(Utility):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, default='Indonesia')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)

    def __str__(self):
        return self.country


class Payment(Utility):
    TYPE_BANK_TRANSFER = 'bank-transfer'
    PAYMENT_TYPES = (
        (TYPE_BANK_TRANSFER, 'Bank Transfer'),
    )
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=100, decimal_places=2)
    payment_type = models.CharField(max_length=100, default=TYPE_BANK_TRANSFER, choices=PAYMENT_TYPES)
    is_paid = models.BooleanField(default=False)
    note = models.TextField()

    def __str__(self):
        return self.sale.sale_number


class SaleItem(Utility):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    quantity = models.PositiveIntegerField(default=1)
    note = models.TextField()

    def __str__(self):
        return self.name



