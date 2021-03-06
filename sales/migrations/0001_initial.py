# Generated by Django 2.2.3 on 2019-07-25 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0002_auto_20190725_1623'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_customer_is_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('sale_number', models.CharField(max_length=100)),
                ('tax', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('bill_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('change_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('status', models.CharField(choices=[('fulfilled', 'Fulfilled'), ('unfulfilled', 'Unfulfilled'), ('finish', 'Finish')], default='unfulfilled', max_length=100)),
                ('note', models.TextField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('country', models.CharField(default='Indonesia', max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=100)),
                ('sale', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaleItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('note', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=100)),
                ('payment_type', models.CharField(choices=[('bank-transfer', 'Bank Transfer')], default='bank-transfer', max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('note', models.TextField()),
                ('sale', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
