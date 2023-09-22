from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', signin,name="signin"),
    path('signout/', signout,name="signout"),
    path('choose_role/',choose_role,name="choose_role"),
    path('otp_verify/',otp_verify,name="otp_verify"),
    path('create_user_profile/',create_user_profile,name="create_user_profile")
]
