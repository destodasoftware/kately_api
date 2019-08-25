from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product
from sales.models import SaleItem, Payment, Sale, Shipping


# sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
#     amount = models.PositiveIntegerField(default=0)
#     payment_type = models.CharField(max_length=100, default=TYPE_BANK_TRANSFER, choices=PAYMENT_TYPES)
#     is_paid = models.BooleanField(default=False)
#     note = models.TextField()

def update_payment(sale):
    payment = Payment.objects.get(sale=sale)
    payment.amount = sale.total()
    payment.save()

def create_payment(sale):
    Payment.objects.create(
        sale=sale,
        is_paid=False,
        amount=sale.total()
    )

@receiver(post_save, sender=Sale)
def save_sale(sender, instance, created, **kwargs):
    print('Invoke save_sale')
    if created:
        create_payment(instance)
    else:
        update_payment(instance)


@receiver(post_save, sender=SaleItem)
def save_saleitem(sender, instance, created, **kwargs):
    update_payment(instance.sale)


@receiver(post_save, sender=Shipping)
def save_shipping(sender, instance, created, **kwargs):
    # print(instance.sale)
    update_payment(instance.sale)


