# Generated by Django 4.1.5 on 2023-01-18 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0006_customer_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='client',
        ),
        migrations.RemoveField(
            model_name='order',
            name='inventory',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
