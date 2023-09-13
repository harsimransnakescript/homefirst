from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', signin,name="signin"),
    path('signout/', signout,name="signout"),
]