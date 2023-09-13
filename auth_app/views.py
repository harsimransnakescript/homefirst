from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login ,logout

def signin(request):
    if request.method=="POST":
        email=request.POST.get("email")
        otp="1234"
        try:
            user_obj=User.objects.get(email=email)
            if otp == user_obj.login_otp:
                login(request, user_obj)
                print("its done")
                return redirect("/")
            else:
                print("wrong otp")

        except:
            user=request.POST.get("user")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            name=request.POST.get("name")
            mail_user_obj=User.objects.filter(email=email) 
            if not mail_user_obj:
                phone_user_obj=User.objects.filter(phone=phone)
                if not phone_user_obj:
                    user = User.objects.create_user( email=email,username1=user,phone=phone,first_name=name)
                    user.save()
                else:
                    print("user with this number already exists")
            else:
                print("user with this email already exists")
    return render(request,"auth_templates/login.html")


def signout(request):
    logout(request)
    return redirect('signin')

