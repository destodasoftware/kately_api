from django.db import models

from utils.models import Utility


class Customer(Utility):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name
