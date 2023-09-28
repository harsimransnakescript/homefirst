from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
import csv
import pandas as pd
from django.http import HttpResponse,HttpResponseBadRequest
import os
import openpyxl
from openpyxl_image_loader import SheetImageLoader
from django.conf import settings
import requests
import asana
from dotenv import load_dotenv
import os
load_dotenv()

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
    # Load the Excel File and the sheet
    xlsx_path = '/Users/apple/Downloads/Homefirst  DME Catalog.xlsx'
    pxl_doc = openpyxl.load_workbook(xlsx_path)
    sheet_name = 'Incontinence Tier 1'
    sheet = pxl_doc[sheet_name]

    start_row = 2  # Assuming row 1 is for headers, adjust if needed
    end_row = 1
    start_column = 1  # Assuming images are in column A, adjust if needed
    end_column = 1  # Assuming images are in column A, adjust if needed

    # Load the image_loader
    image_loader = SheetImageLoader(sheet)
    for row in range(start_row, end_row + 1):
        for column in range(start_column, end_column + 1):
            cell = sheet.cell(row=row, column=column)

            # Check if the cell has an image
            if cell.has_image:
                image = image_loader.get(cell.coordinate)
                media_folder = os.path.join(settings.MEDIA_ROOT, 'products/')

                # Create the media folder if it doesn't exist
                os.makedirs(media_folder, exist_ok=True)

                # Generate a unique image name (e.g., using the cell coordinates)
                image_name = f'image_{cell.coordinate.replace(" ", "_")}.png'
                image_path = os.path.join(media_folder, image_name)

                # Save the image to the media folder
                image.save(image_path)

                print(f"Image saved to: {image_path}")
            else:
                print(f"No image found in cell {cell.coordinate}")

    sheet_name = "Incontinence Tier 2 &3"
    # Read the Excel file
    df = pd.read_excel("/Users/apple/Downloads/Homefirst  DME Catalog.xlsx", sheet_name=sheet_name)
    print(df)
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


@login_required
def order_sample(request):

    categories = Categories.objects.all()
    sample_product_names = SampleProductsModel.objects.values_list('name', flat=True)
    
    if request.method=='POST':
        category = request.POST.get("category")
        sample_item = request.POST.get("sample_item")
        delivery_method = request.POST.get("delivery_method")
        shipping_address = request.POST.get("shipping_address")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        mobile_phone = request.POST.get("mobile_phone")
        
        try:
            category = Categories.objects.get(id=category)
        except Categories.DoesNotExist:
            category = None

        try:
            sample_item = SampleProductsModel.objects.get(name=sample_item)
        except SampleProductsModel.DoesNotExist:
            sample_item = None
            
        order = OrderSample(
            category=category, 
            sample_item=sample_item,
            delivery_method=delivery_method,
            shipping_address=shipping_address,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            mobile_phone=mobile_phone
        )
        order.save()
        task = f"Order: {category} - {sample_item}, " \
           f"Delivery Method: {delivery_method}, " \
           f"Shipping Address: {shipping_address}, " \
           f"First Name: {first_name}, " \
           f"Last Name: {last_name}, " \
           f"Gender: {gender}, " \
           f"Mobile Phone: {mobile_phone}"
        
        url = "https://app.asana.com/api/1.0/tasks?opt_fields=&opt_pretty=true"
        payload = { "data": {
                          
                                "projects": ["1205600469702396"],
                                "name": str(task),
                            
                            } }
        headers = {
                        "accept": "application/json",
                        "content-type": "application/json",
                        "authorization": os.environ.get('ASANA_TOKEN')
                    }
        
        response = requests.post(url, json=payload, headers=headers)

    return render(request, 'main_templates/order_sample_form.html', {'categories': categories, 'sample_product_names': sample_product_names,})

