from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("products/",products,name="products"),
    path("loadcsv/",import_csv_to_model,name="loadcsv"),
    path("loadexcel/",import_excel_to_model,name="loadexcel")
]
