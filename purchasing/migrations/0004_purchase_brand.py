# Generated by Django 2.2.3 on 2019-08-21 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20190805_1832'),
        ('purchasing', '0003_purchase_purchase_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Brand'),
        ),
    ]
