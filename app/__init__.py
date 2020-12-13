from flask import Flask
from orange_sms import sms
from config import allowed_users, orange_credentials, twilio_credentials
from twilio.rest import Client

app = Flask(__name__)
sms = sms(orange_credentials["login"], orange_credentials["password"])
twilio_client = Client(twilio_credentials["account_sid"], twilio_credentials["auth_token"])

def twilio(user, text):
    message = twilio_client.messages.create(
        messaging_service_sid = twilio_credentials["messaging_service_sid"],
        body = text,
        to = "+33" + allowed_users[users][1::]
    )

    return message.error_code, message.error_message, message.price

from app import routes
