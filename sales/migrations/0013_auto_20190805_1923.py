# Generated by Django 2.2.3 on 2019-08-05 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_saleitem_is_available'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='is_verified',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='total',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='is_discount_percent',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='total',
        ),
    ]
