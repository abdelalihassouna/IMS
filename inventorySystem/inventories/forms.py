from django.forms import ModelForm, forms
from .models import Inventory, Sales, StockLoad
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InventoryUpdateForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "cost_per_item", "quantity_in_stock", "quantity_sold"]

class AddInventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = ["name", "cost_per_item", "quantity_in_stock"]

class SalesForm(ModelForm):
    sold_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    class Meta:
        model = Sales
        fields = ['name', 'qty_sold', 'sold_date']

    def delete(self, instance):
        instance.delete()

class StockLoadForm(ModelForm):
    load_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    class Meta:
        model = StockLoad
        fields =  ['name', 'quantity_loaded', 'load_date']

class DailyPrintForm(forms.Form):
    class Meta:
        start_date = forms.DateInput()
        end_date = forms.DateInput()
        fields = ['name', 'um', 'last_stock', 'daily_load', 'current_stock', 'daily_sold', 'daily_stock', 'info', 'daily_revenue'  ]

class CreateNewUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user