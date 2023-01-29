from django.contrib import admin
from .models import Inventory,Sales,StockLoad

# Register your models here.
admin.site.register(Inventory)
admin.site.register(Sales)
admin.site.register(StockLoad)

