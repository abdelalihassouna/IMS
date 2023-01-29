# Generated by Django 4.1.5 on 2023-01-19 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0008_sales_rename_sales_inventory_revenue_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
