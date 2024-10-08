# Generated by Django 4.1.5 on 2023-01-18 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventories', '0007_remove_order_client_remove_order_inventory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='sales',
            new_name='revenue',
        ),
        migrations.DeleteModel(
            name='InventorySales',
        ),
        migrations.AddField(
            model_name='sales',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventories.inventory'),
        ),
    ]
