from django.db import models

from products.models import Product, Brand
from utils.models import Utility


class Purchase(Utility):
    purchase_number = models.CharField(unique=True, max_length=100, blank=True, null=True)
    brand = models.ForeignKey(Brand, blank=True, null=True, on_delete=models.SET_NULL)
    purchase_date = models.DateField(blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    note = models.TextField(blank=True)
    is_adjusment = models.BooleanField(default=False)

    def __str__(self):
        return self.purchase_number


class PurchaseItem(Utility):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name







