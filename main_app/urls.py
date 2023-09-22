from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("products/",products,name="products"),
    path("loadcsv/",import_csv_to_model,name="loadcsv"),
    path("loadexcel/",import_excel_to_model,name="loadexcel"),
    path('order-sample/', order_sample, name='order_sample'),
    path('authorization-status/', authorization_status, name='authorization_status'),
    path('sample-request-success/', sample_request_success, name='sample_request_success'),
]

