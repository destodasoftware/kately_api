# Generated by Django 2.2.3 on 2019-08-08 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0018_auto_20190808_0411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('cash', 'Cash'), ('bank-transfer', 'Bank Transfer')], default='bank-transfer', max_length=100),
        ),
    ]
