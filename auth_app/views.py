from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login ,logout

def choose_role(request):
    return render(request,"auth_templates/choose-role.html")

def signin(request):
    if request.method=="POST":
        email=request.POST.get("email")
        otp="1234"
        try:
            user_obj=User.objects.get(email=email)
            if otp == "1234":
                login(request, user_obj)
                return redirect("/")
            else:
                print("wrong otp")

        except:
            mail_user_obj=User.objects.filter(email=email) 
            if not mail_user_obj:
                phone_user_obj=User.objects.filter(phone=phone)
                if not phone_user_obj:
                    user = User.objects.create_user( email=email,phone=phone)
                    user.save()
                else:
                    print("user with this number already exists")
            else:
                print("user with this email already exists")
    return render(request,"auth_templates/login.html")

def otp_verify(request):
    return render(request,"auth_templates/verification-otp.html")


def signout(request):
    logout(request)
    return redirect('signin')

