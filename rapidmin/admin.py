from django.contrib import admin

from products.models import Category, Brand, Product
from sales.models import Sale, SaleItem, Shipping, Payment
from users.models import Customer

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Shipping)
admin.site.register(Payment)
