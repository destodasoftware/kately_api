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


class Article(Utility):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(Utility):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sku = models.CharField(blank=True, null=True, max_length=30, unique=True)
    name = models.CharField(max_length=100)
    cost = models.DecimalField(decimal_places=2, max_digits=100)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    stock = models.PositiveIntegerField()
    minimum_stock = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

