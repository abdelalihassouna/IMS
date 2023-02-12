from django.db import models

# Create your models here.

class Inventory(models.Model):
    um = (("kom","kom"),
          ("kg","kg"),
          ("lit","lit")
          )
    name = models.CharField(max_length=200, null=False, blank=False)
    cost_per_item = models.DecimalField(max_digits=19, decimal_places=3, null=False, blank=False)
    quantity_in_stock = models.IntegerField(null=False, blank=False)
    quantity_sold = models.IntegerField(null=False, blank=False, default=0)
    revenue = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False, default=0)
    stock_date = models.DateField(auto_now_add=True)
    last_sales_date = models.DateField(auto_now=True)
    unit_of_measure = models.CharField(max_length=3, choices=um, default="kom")
    
    def __str__(self) -> str:
        return self.name
      
class Sales(models.Model):
    name = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    qty_sold = models.IntegerField()
    sold_date = models.DateField()
    
    def __str__(self):
        return f"{self.name}"

class StockLoad(models.Model):
    name = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity_loaded = models.IntegerField()
    load_date = models.DateField()
    
    def __str__(self):
        return f"{self.name}"



        
# class Customer(models.Model):
#     name = models.CharField(max_length=200, null=False, blank=False)
#     email = models.CharField(max_length=200, null=False, blank=False)
#     phone_number = models.CharField(max_length=200, null=False, blank=False)
#     address = models.CharField(max_length=200, null=False, blank=False)
#     city = models.CharField(max_length=200, null=False, blank=False)
#     state = models.CharField(max_length=200, null=False, blank=False)
#     country = models.CharField(max_length=200, null=False, blank=False)
#     zip_code = models.CharField(max_length=200, null=False, blank=False)

#     def __str__(self) -> str:
#         return self.name

# class Order(models.Model):
    # client = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    # quantity = models.IntegerField(null=False, blank=False)
    # order_date = models.DateField(auto_now_add=True)

    # def __str__(self) -> str:
    #     return self.inventory.name

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
#     quantity = models.IntegerField(null=False, blank=False)
#     order_date = models.DateField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.inventory.name

# class OrderItemSales(models.Model):
#     order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
#     inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
#     quantity = models.IntegerField(null=False, blank=False)
#     sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
#     sales_date = models.DateField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.inventory.name

# class OrderSales(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
#     quantity = models.IntegerField(null=False, blank=False)
#     sales = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
#     sales_date = models.DateField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.inventory.name

# class InventorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Inventory
#         fields = '__all__'
    
#     def create(self, validated_data):
#         return Inventory.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.cost_per_item = validated_data.get('cost_per_item', instance.cost_per_item)
#         instance.quantity_in_stock = validated_data.get('quantity_in_stock', instance.quantity_in_stock)
#         instance.quantity_sold = validated_data.get('quantity_sold', instance.quantity_sold)
#         instance.sales = validated_data.get('sales', instance.sales)
#         instance.stock_date = validated_data.get('stock_date', instance.stock_date)
#         instance.last_sales_date = validated_data.get('last_sales_date', instance.last_sales_date)
#         instance.save()
#         return instance
    
#     def delete(self, instance):
#         instance.delete()

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'
    
#     def create(self, validated_data):
#         return Customer.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.email = validated_data.get('email', instance.email)
#         instance.phone_number = validated_data.get('phone_number', instance.phone_number)
#         instance.address = validated_data.get('address', instance.address)
#         instance.city = validated_data.get('city', instance.city)
#         instance.state = validated_data.get('state', instance.state)
#         instance.country = validated_data.get('country', instance.country)
#         instance.zip_code = validated_data.get('zip_code', instance.zip_code)
#         instance.save()
#         return instance
    
#     def delete(self, instance):
#         instance.delete()
    
# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
    
#     def create(self, validated_data):
#         return Order.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.inventory = validated_data.get('inventory', instance.inventory)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.order_date = validated_data.get('order_date', instance.order_date)
#         instance.save()
#         return instance
    
#     def delete(self, instance):
#         instance.delete()
    
# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'
    
#     def create(self, validated_data):
#         return OrderItem.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.order = validated_data.get('order', instance.order)
#         instance.inventory = validated_data.get('inventory', instance.inventory)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.order_date = validated_data.get('order_date', instance.order_date)
#         instance.save()
#         return instance
    
#     def delete(self, instance):
#         instance.delete()

# class OrderItemSalesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItemSales
#         fields = '__all__'
    
#     def create(self, validated_data):
#         return OrderItemSales.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.order_item = validated_data.get('order_item', instance.order_item)
#         instance.inventory = validated_data.get('inventory', instance.inventory)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.sales = validated_data.get('sales', instance.sales)
#         instance.sales_date = validated_data.get('sales_date', instance.sales_date)
#         instance.save()
#         return instance
    
#     def delete(self, instance):
#         instance.delete()

# class OrderSalesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderSales
#         fields = '__all__'
    
#     def create(self, validated_data):
#         return OrderSales.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.order = validated_data.get('order', instance.order)
#         instance.inventory = validated_data.get('inventory', instance.inventory)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.sales = validated_data.get('sales', instance.sales)
#         instance.sales_date = validated_data.get('sales_date', instance.sales_date)
#         instance.save()
#         return instance
    
#     def delete(self, instance):
#         instance.delete()