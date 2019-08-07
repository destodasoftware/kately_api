from django.db import models
from django.db.models.signals import post_save

from products.models import Product
from sales.models import SaleItem
