# Generated by Django 2.2.3 on 2019-08-08 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0022_auto_20190808_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='cost',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shipping',
            name='courier_service',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shipping',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
