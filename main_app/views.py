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



# View to display the sample request form
@login_required
def order_sample(request):
    if request.method == 'POST':
        # Get data from the POST request
        sample_id = request.POST.get('sample_id')
        quantity = request.POST.get('quantity')
        shipping_address = request.POST.get('shipping_address')
        special_instructions = request.POST.get('special_instructions')

        try:
            sample = Sample.objects.get(pk=sample_id)
        except Sample.DoesNotExist:
            return HttpResponseBadRequest("Sample not found")

        # Create a new sample request
        sample_request = SampleRequest(
            requester=request.user.requester,  # Assuming you have user authentication
            sample=sample,
            quantity=quantity,
            shipping_address=shipping_address,
            special_instructions=special_instructions,
            status='Pending'  # You can set the initial status as needed
        )
        sample_request.save()

        return redirect('/')  # Redirect to a success page

    # Retrieve a list of available samples to display in the form
    samples = Sample.objects.all()
    
    return render(request, 'main_templates/order_sample.html', {'samples': samples})

# View to list sample request statuses
@login_required
def authorization_status(request):
    sample_requests = SampleRequest.objects.filter(requester=request.user.requester)  # Filter by the current requester
    return render(request, 'main_templates/authorization_status.html', {'sample_requests': sample_requests})

# View to display sample request success page
@login_required
def sample_request_success(request):
    return render(request, 'main_templates/sample_request_success.html')


