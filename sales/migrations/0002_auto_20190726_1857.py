# Generated by Django 2.2.3 on 2019-07-26 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customer_is_delete'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='bill_amount',
            new_name='total',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='change_amount',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='grand_total',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='note',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='tax',
        ),
        migrations.AddField(
            model_name='sale',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_number',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='TaxSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('is_percent', models.BooleanField(default=True)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Customer')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CashSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('bill_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('change_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
