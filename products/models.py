from django.db import models

from utils.models import Utility


class Category(Utility):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Brand(Utility):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(Utility):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    root = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    sku = models.CharField(blank=True, null=True, max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    cost = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(blank=True, null=True)
    minimum_stock = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

