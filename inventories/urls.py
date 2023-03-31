from django.urls import path
from .views import *

urlpatterns = [
    path("", inventoryList, name="inventorylist"),
    path("ProductView/<int:pk>/", per_product_view, name="per_product"),
    path("ProductUpdate/<int:pk>/", update, name="product_update"),
    path("Delete/<int:pk>/", delete, name="product_delete"),
    path("Ddd/", add_product, name="product_add"),
    path("Dashboard/", dashboard, name="dashboard"),
    path("Sales/", sales, name="sales"),
    path("StockLoad/", stock_load, name="stock_load"),
    path("Report/", daily_print, name="report"),
    # path("Upload", upload_pdf, name="upload_pdf"),
]
