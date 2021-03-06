# Generated by Django 2.2.3 on 2019-07-30 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20190730_0742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('purchase_number', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('supplier', models.CharField(blank=True, max_length=100, null=True)),
                ('note', models.TextField()),
                ('is_adjusment', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('create', models.DateField(auto_now_add=True)),
                ('update', models.DateField(auto_now=True)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchasing.Purchase')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
