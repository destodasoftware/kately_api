from django.db import models

from products.models import Product, Brand
from users.models import Customer
from utils.models import Utility


class Sale(Utility):
    STATUS_OPEN = 'open'
    STATUS_ARCHIEVED = 'archieved'
    STATUS_CANCEL = 'cancel'
    STATUS_CHOICES = (
        (STATUS_OPEN, 'Open'),
        (STATUS_ARCHIEVED, 'Archieved'),
        (STATUS_CANCEL, 'Cancel'),
    )

    sale_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_OPEN)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    sale_date = models.DateField(blank=True, null=True)

    def total(self):
        lines_total = []
        if self.saleitem_set.all():
            for item in self.saleitem_set.all():
                lines_total.append(item.total())

        try:
            shipment_cost = self.shipping.cost
            lines_total.append(shipment_cost)
        except:
            pass

        return sum(lines_total)


    def __str__(self):
        return self.sale_number


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
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, blank=True, null=True)
    country = models.CharField(max_length=100, default='Indonesia', blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(blank=True, null=True, max_length=100)
    courier_service = models.CharField(blank=True, null=True, max_length=100)
    cost = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.country


class Payment(Utility):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.sale.sale_number


class SaleItem(Utility):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.PositiveIntegerField(default=0)
    is_percent = models.BooleanField(default=False)

    def price_after_discount(self):
        if self.discount:
            if self.is_percent:
                return self.price * (self.discount / 100)
            else:
                return self.price - self.discount
        return self.price

    def total(self):
        return self.price_after_discount() * self.quantity

    def __str__(self):
        return self.product.name





