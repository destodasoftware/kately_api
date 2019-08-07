from django.db import models

from utils.models import Utility


class Customer(Utility):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    customer_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True, default='No Name')
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.customer_number




