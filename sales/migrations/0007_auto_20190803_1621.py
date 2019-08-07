# Generated by Django 2.2.3 on 2019-08-03 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_auto_20190802_0454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='country',
            field=models.CharField(blank=True, default='Indonesia', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='postal_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='province',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='sale',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Sale'),
        ),
    ]
