# Generated by Django 4.1.5 on 2023-01-21 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0014_rename_date_sales_sold_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='quantity_sold',
            new_name='qty_sold',
        ),
    ]
