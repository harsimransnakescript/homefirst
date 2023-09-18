from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    products=ProductsModel.objects.all()
    return render(request,"main_templates/home.html",{"products":products})