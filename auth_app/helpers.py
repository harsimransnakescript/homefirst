from random import randint
from django.core.mail import send_mail
from auth_app.models import *
from twilio.rest import Client
from django.conf import settings


def random_with_N_digits():
    range_start = 10 ** (4-1)
    range_end = (10 ** 4)-1
    return randint(range_start,range_end)

def generate_otp():
    # Generate a random OTP using the random_with_N_digits function
    return str(random_with_N_digits())


def send_email_verification_otp(email):
    otp = generate_otp()
    otp_model, created = Otp.objects.get_or_create(email=email)
    otp_model.otp_code = otp
    otp_model.save()

    subject = "Email Verification OTP"
    message = f"Your email verification OTP: {otp}"
    send_mail(subject, message, "tu716599@gmail.com", [email])

    return otp  # Return the generated OTP value


def send_phone_verification_otp(recipient_number):
    otp = generate_otp()
    otp_model, created = Otp.objects.get_or_create(phone_number=recipient_number)
    otp_model.otp_code = otp
    otp_model.save()

    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    body = f"Your phone verification OTP: {otp}"
    from_number = settings.TWILIO_PHONE_NUMBER

    message = client.messages.create(
        body=body, from_=from_number, to=recipient_number
    )
    print(f"OTP sent to {recipient_number} with message SID: {message.sid}")

    return otp  # Return the generated OTP value

