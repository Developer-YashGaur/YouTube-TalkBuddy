import random
import string
from django.conf import settings
from twilio.rest import Client
import environ

env = environ.Env()
environ.Env.read_env()

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def send_otp_phone(mobileNumber, otp):
    account_sid = env("TWILIO_ACCOUNT_SID")  # Replace with your Twilio account SID
    auth_token = env("TWILIO_AUTH_TOKEN")  # Replace with your Twilio auth token
    twilio_phone_number = env("TWILIO_VERIFIED_NUMBER")  # Replace with your Twilio phone number

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=twilio_phone_number,
        # to=mobileNumber
        to="+919257741067"
    )
