from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
import csv

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


@login_required
def products(request):
    products = ProductsModel.objects.all()
    return render(request, "main_templates/products.html", {"products": products})
