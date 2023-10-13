from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("products/",products,name="products"),
    path("loadcsv/",import_csv_to_model,name="loadcsv"),
    path("form/",form_view,name="form"),
    path("ticket-history/",ticket_form,name="ticket-history"),
    path("ticket-details/",ticket_details,name="ticket-details"),
    path('ticket-solved/', ticket_solved, name="ticket-solved"),
    path("loadexcel/",import_excel_to_model,name="loadexcel"),
    path('order-sample-form/', order_sample, name='order-sample-form'),
    path('create_authorization_status/',create_authorization_status,name='create_authorization_status')

]

