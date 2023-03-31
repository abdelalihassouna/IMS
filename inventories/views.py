from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from .models import Inventory
#Update form import
from .forms import *
# flash messages
from django.contrib import messages
# dataframe
from django_pandas.io import read_frame
# plotly
import plotly
import plotly.express as px
import pandas as pd
# json
import json
from django.utils import timezone
from datetime import timedelta
from django.db import models,transaction
from django.db.models import Sum, F,Case, When, IntegerField
from django.views import View
from django.template.loader import get_template
# from .utils import render_to_pdf
from django.views import generic
from .decorators import *
import requests
from django.conf import settings
import pdfminer.high_level
import io
import pytesseract
from PIL import Image
import re

@login_required(login_url='login')
@admin_only
def inventoryList(request):
    inventories = Inventory.objects.all()
    context = {
        "inventories": inventories
    }
    return render(request, "inventories/inventory_list.html", context=context)

@login_required(login_url='login')
@admin_only
def per_product_view(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, "inventories/per_product.html", context=context)

@login_required(login_url='login')
@admin_only
def update(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        updateForm = InventoryUpdateForm(data=request.POST)
        if updateForm.is_valid():
            inventory.name = updateForm.data['name']
            inventory.quantity_in_stock = updateForm.data['quantity_in_stock']
            inventory.quantity_sold = updateForm.data['quantity_sold']
            inventory.cost_per_item = updateForm.data['cost_per_item']
            inventory.quantity_sold = float(inventory.cost_per_item) * float(inventory.quantity_sold)
            inventory.save()
            messages.success(request, "Update Successful")
            return redirect(f"/inventory") #/per_product_view/{pk}/ se volessi tornare alle info del prodotto usando pk
    else:
        updateForm = InventoryUpdateForm(instance=inventory)

    return render(request, "inventories/inventory_update.html", {'form' : updateForm})

@login_required(login_url='login')
@admin_only
def delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, "Inventory Deleted")
    return redirect("/inventory")

@login_required(login_url='login')
@admin_only
def add_product(request):
    if request.method == "POST":
        updateForm = AddInventoryForm(data=request.POST)
        if updateForm.is_valid():
            new_invetory = updateForm.save(commit=False)
            # new_invetory.sales = float(updateForm.data['cost_per_item']) * float(updateForm.data['quantity_sold'])
            new_invetory.save()
            messages.success(request, "Successfully Added Product")
            return redirect(f"/inventory/")
    else:
        updateForm = AddInventoryForm()

    return render(request, "inventories/inventory_add.html", {'form' : updateForm})

@login_required(login_url='login')
@admin_only
def dashboard(request):
    inventories = Inventory.objects.all()
    df = read_frame(inventories)
    
    # sales graph
    # print(df.columns)
    sales_graph_df = df.groupby(by="last_sales_date", as_index=False, sort=False)['revenue'].sum()
    # print(sales_graph_df.revenue)
    # print(sales_graph_df.columns)
    sales_graph = px.line(sales_graph_df, x = sales_graph_df.last_sales_date, y = sales_graph_df.revenue, title="Sales Trend")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

    
    # best performing product
    best_performing_product_df = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_performing_product = px.bar(best_performing_product_df, 
                                    x = best_performing_product_df.index, 
                                    y = best_performing_product_df.quantity_sold, 
                                    title="Best Performing Product"
                                )
    best_performing_product = json.dumps(best_performing_product, cls=plotly.utils.PlotlyJSONEncoder)


    # best performing product in sales
    sales_graph_df_per_product_df = df.groupby(by="name", as_index=False, sort=False)['revenue'].sum()
    best_performing_product_per_product = px.pie(sales_graph_df_per_product_df, 
                                    names = "name", 
                                    values = "revenue", 
                                    title="Product Performance By Sales",
                                    # https://plotly.com/python/discrete-color/
                                    color_discrete_sequence=px.colors.qualitative.Bold,
                                )
    best_performing_product_per_product = json.dumps(best_performing_product_per_product, cls=plotly.utils.PlotlyJSONEncoder)


     # Most Product In Stock
    most_product_in_stock_df = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    most_product_in_stock = px.pie(most_product_in_stock_df, 
                                    names = most_product_in_stock_df.index, 
                                    values = most_product_in_stock_df.quantity_in_stock, 
                                    title="Most Product In Stock"
                                )
    most_product_in_stock = json.dumps(most_product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "sales_graph": sales_graph,
        "best_performing_product": best_performing_product,
        "most_product_in_stock": most_product_in_stock,
        "best_performing_product_per_product": best_performing_product_per_product
    }

    return render(request,"inventories/dashboard.html", context=context)

@login_required(login_url='login')
# @user_passes_test(employee_check)
def sales(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                name = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('qty_sold')
                date = form.cleaned_data.get('sold_date')
                # product = Inventory.objects.select_for_update().get(name=name)
                product = Inventory.objects.get(name=name)
                if product.quantity_in_stock < quantity or quantity == 0:
                    form.add_error('quantity_sold',"Insufficient Stock")
                    return render(request, "inventories/sales.html", {'form': form})
                else:
                    product.quantity_in_stock -= quantity
                    product.quantity_sold += quantity
                    product.revenue += product.cost_per_item * quantity
                    product.last_sales_date = date
                    product.save()
                    sale = form.save(commit=False)
                    sale.save()
                    messages.success(request, "Sales Successful")
                    return render(request, "inventories/sales.html", {'form': form})
                    # return redirect("/inventories/sales.html/", {'form': form})
        else:
            messages.error(request, "Sales Unsuccessful")
            return render(request, "inventories/sales.html", {'form': form})
    else:
        # messages.success(request, "Sales Unsuccessful")
        form = SalesForm()
        return render(request, "inventories/sales.html", {'form': form})

@login_required(login_url='login')
@admin_only
def stock_load(request):
    if request.method == 'POST':
        form = StockLoadForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                name = form.cleaned_data.get('name')
                quantity = form.cleaned_data.get('quantity_loaded')
                product = Inventory.objects.get(name=name)
                product.quantity_in_stock += quantity
                product.stock_date = form.cleaned_data.get('load_date')
                product.save()
                stock_load = form.save(commit=False)
                stock_load.save()
                messages.success(request, "Stock Load Successful")
                return render(request, "inventories/stock_load.html", {'form': form})
        else:
            messages.error(request, "Stock Load Unsuccessful")
            return render(request, "inventories/stock_load.html", {'form': form})
    else:
        form = StockLoadForm()
        return render(request, "inventories/stock_load.html", {'form': form})

@login_required(login_url='login')
@admin_only
def daily_print(request):
    today = timezone.now()
    inventory = Inventory.objects.annotate(
    daily_sales=Sum(Case(When(sales__sold_date=today, then='sales__qty_sold'), output_field=IntegerField(), default=0)),
    daily_load=Sum(Case(When(stockload__load_date=today, then='stockload__quantity_loaded'), output_field=IntegerField(), default=0)),
    actual_stock = F('quantity_in_stock') + F('daily_sales'),
    daily_stock=F('actual_stock')+F('daily_load'),
    daily_revenue=(F('cost_per_item')*F('daily_sales')),
    tot_daily = F('daily_stock')-F('daily_sales')
).values('name', 'unit_of_measure' ,'actual_stock', 'daily_load', 'daily_stock','daily_sales', 'tot_daily', 'daily_revenue')
    # Calcola il totale delle vendite giornaliere
    total_daily_sales = inventory.aggregate(total=Sum('daily_sales'))['total']

    # Aggiungi il totale alla fine della lista inventory
    inventory = list(inventory)
    inventory.append({'name': 'Totale', 'daily_sales': total_daily_sales})
    
    return render(request, "inventories/print.html",  {'report': inventory, 'today':today})

@never_cache
@unauthenticated_user
def login(request):
    # non funziona devo capire perchè
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('group')
        user = authenticate(request, username=username, password=password, role=role)
        if user is not None:
            login(request, user, role)
            return redirect('/inventory')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    
    return render(request, "login.html", context)

@unauthenticated_user
def register(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name="employees")
                user.groups.add(group)
                messages.success(request, 'Account was created for ' + username)
                return redirect("login")
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    context = {'form': form}
    return render(request, "inventory_system/register.html", context)

@never_cache                
def logoutUser(request):
    logout(request)
    return redirect('login')

@user_passes_test(employee_check)
def userProfile(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        user = authenticate(request, username=username, password=password, role=role)
        if user is not None and user.role == 'employees':
            login(request, user)
            return redirect('sales')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'inventory_system/profile.html')

# def upload_pdf(request):
#     if request.method == 'POST':
#         pdf_file = request.FILES['pdf_file']
#         text = extract_text_from_pdf(pdf_file)
#         product_data = extract_product_data(text)
#         save_products_to_stock(product_data)
#         messages.success(request, 'Prodotti caricati correttamente.')
#     return render(request, 'inventories/upload_pdf.html')

# def extract_text_from_pdf(pdf_file):
#     with io.BytesIO(pdf_file.read()) as pdf_buffer:
#         extracted_text = pdfminer.high_level.extract_text(pdf_buffer)
#     return extracted_text

# def extract_product_data(text):
#     product_data = []
#     for line in text.splitlines():
#         if line.startswith('Prodotto'):
#             product = {}
#             product['name'] = line.split(':')[1].strip()
#         elif line.startswith('Descrizione'):
#             product['description'] = line.split(':')[1].strip()
#         elif line.startswith('Prezzo'):
#             product['price'] = line.split(':')[1].strip()
#         elif line.startswith('Quantità'):
#             product['quantity'] = int(line.split(':')[1].strip())
#             product_data.append(product)
#     return product_data

# def save_products_to_stock(product_data):
#     for product in product_data:
#         # Crea un oggetto di prodotto e salvalo nel database
#         p = Product(name=product['name'], description=product['description'], price=product['price'])
#         p.save()
#         # Aggiungi il prodotto al magazzino e aggiorna la quantità disponibile
#         s, created = Stock.objects.get_or_create(product=p)
#         s.quantity += product['quantity']
#         s.save()