from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login ,logout
from django.contrib.auth import authenticate
from django.urls import reverse
from auth_app import helpers


def choose_role(request):
    if request.method == "POST":
        role = request.POST.get("role")
        print(role)
        url = reverse("signin") + f"?role={role}"
        return redirect(url)
    return render(request, "auth_templates/choose-role.html")

def signin(request):
    selected_role = request.GET.get("role")
    if request.method == "POST":
        selected_role = request.POST.get("role")
        if selected_role == "case_manager":
            email = request.POST.get("email")
            if User.objects.filter(email=email).exists():
                return render(request, "auth_templates/login.html", {"role": selected_role, "error_message": "Email already exists."})
            else:
                helpers.send_email_verification_otp(email)
                return redirect("otp_verify")

        else:
            phone = request.POST.get("phone")
            print(phone)
          
            if User.objects.filter(phone=phone).exists():
                return render(request, "auth_templates/login.html", {"role": selected_role, "error_message": "Phone number already exists."})
            else:
                helpers.send_phone_verification_otp(phone)
                return redirect("otp_verify")

    return render(request, "auth_templates/login.html",{"role":selected_role})

def otp_verify(request):
    
    return render(request,"auth_templates/verification-otp.html")


def signout(request):
    logout(request)
    return redirect('signin')

