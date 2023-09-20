from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
import csv
import pandas as pd

from django.http import HttpResponse


# Create your views here.
@login_required
def home(request):
    products = ProductsModel.objects.all()
    return render(request, "main_templates/home.html", {"products": products})


def import_csv_to_model(csv_file_path):
    csv_file_path = "/Users/apple/Downloads/Homefirst DME Catalog.csv"

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            product = ProductsModel(
                group=row["CATEGORY"],
                name=row["Product Name"],
                image=None,
                specifications=row["DESCRIPTION"],
                other_info=row["PRODUCT FEATURES"],
                price=None,
            )

            product.save()
        return HttpResponse("Categories Added")
    
def import_excel_to_model(excel_file_path):
    sheet_name = "Incontinence Tier 2 &3"
    # Read the Excel file
    df = pd.read_excel("/Users/apple/Downloads/Homefirst  DME Catalog.xlsx",sheet_name=sheet_name)

    for index, row in df.iterrows():
        print(row)
        product = ProductsModel(
            group=row["Category"],
            name=row["Item Name"],
            image=None,  
            specifications=row["Brand"],
            other_info=row["Dimension"],
            price=None, 
            category_id=None, 
        )

        product.save()

    return HttpResponse("Categories Added")


@login_required
def products(request):
    categories = Categories.objects.all()
    products = ProductsModel.objects.all()

    return render(request, "main_templates/products.html", {"categories": categories, "products": products})
