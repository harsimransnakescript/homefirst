from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse
from auth_app import helpers
from django.contrib import messages
from .models import User, AllowedDomain

def choose_role(request):
    """
    Function handles the selection of a user role.
    """
    if request.method == "POST":
        role = request.POST.get("role")
        # Construct a URL for the signin view, appending the role as a query parameter
        url = reverse("signin") + f"?role={role}"
        return redirect(url)
    return render(request, "auth_templates/choose-role.html")


def signin(request):
    """
    Function for user SignIn and Login
    """
    selected_role = request.GET.get("role")
    if request.method == "POST":
        selected_role = request.POST.get("role")
        if selected_role == "case_manager":
            email = request.POST.get("email")
            email_domain = email.split('@')[-1]
        
            # Check if the email domain is allowed
            try:
                allowed_domain = AllowedDomain.objects.get(domain=email_domain)
            except AllowedDomain.DoesNotExist:
                messages.error(request, f"Only organisation email domain is allowed.")
                return render(request, "auth_templates/login.html", {"role": selected_role})

            # Store the email and send an email verification OTP
            request.session["email"] = email
            email_otp = helpers.send_email_verification_otp(email)
            request.session["email_otp"] = email_otp

            # Redirect to OTP verification page with the selected role
            url = reverse("otp_verify") + f"?role={selected_role}"
            return redirect(url)

        else:
            phone = request.POST.get("phone")

            # Store the phone number and send an phone verification OTP
            request.session["phone"] = phone
            phone_otp = helpers.send_phone_verification_otp(phone)
            request.session["phone_otp"] = phone_otp

            # Redirect to OTP verification page with the selected role
            url = reverse("otp_verify") + f"?role={selected_role}"
            return redirect(url)

    return render(request, "auth_templates/login.html", {"role": selected_role})


def otp_verify(request):
    """
    Function for OTP verification during the sign-in and login process
    """
    selected_role = request.GET.get("role")
    if request.method == "POST":
        digit1 = request.POST.get("digit1")
        digit2 = request.POST.get("digit2")
        digit3 = request.POST.get("digit3")
        digit4 = request.POST.get("digit4")

        entered_code = f"{digit1}{digit2}{digit3}{digit4}"

        selected_role = request.POST.get("role")
        # If selected role is case manager 
        if selected_role == "case_manager":
            email_otp = request.session.get("email_otp")
            email = request.session.get("email")

            if entered_code == email_otp:
                existing_user = User.objects.filter(
                    email=email, is_manager=True
                ).first()

                if existing_user:
                    # If the user exists, log them in and redirect to the homepage
                    login(request, existing_user)
                    return redirect("/")
                else:
                    # If the user doesn't exist, create a new case manager user 
                    user = User.objects.create(
                        username1=email, email=email, is_manager=True
                    )
                    user.save()
                    return redirect("/")
            else:
                # If the entered code is invalid, show an error message
                messages.error(request, "Invalid verification code. Please try again.")        
        #If selected role is patient 
        else:
            phone_otp = request.session.get("phone_otp")
            phone = request.session.get("phone")

            if entered_code == phone_otp:
                existing_user = User.objects.filter(
                    phone=phone, is_patient=True
                ).first()

                if existing_user:
                    # If the user exists, log them in and redirect to the homepage
                    login(request, existing_user)
                    return redirect("/")
                else:
                    # If the user doesn't exist, create a new patient user
                    user = User.objects.create(
                        username1=phone, phone=phone, is_patient=True
                    )
                    user.save()
                    return redirect("/")
            else:
                # If the entered code is invalid, show an error message
                messages.error(request, "Invalid verification code. Please try again.")

    return render(
        request, "auth_templates/verification-otp.html", {"role": selected_role}
    )


def signout(request):
    logout(request)
    return redirect("signin")
