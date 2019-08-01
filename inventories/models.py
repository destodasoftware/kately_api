from django.db import models

from products.models import Product
from utils.models import Utility


class Inventory(Utility):
    inventory_number = models.CharField(unique=True, max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    is_adjusment = models.BooleanField(default=False)

    def __str__(self):
        return self.inventory_number


class InventoryItem(Utility):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name




