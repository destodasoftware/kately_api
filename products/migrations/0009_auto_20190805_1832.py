# Generated by Django 2.2.3 on 2019-08-05 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20190805_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='article',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]