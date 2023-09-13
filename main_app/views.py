from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    products=ProductsModel.objects.all()
    return render(request,"main_templates/home.html",{"products":products})