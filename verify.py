
import os
from twilio.rest import Client
import json
from crud import get_user_by_phone
from model import connect_to_db

if __name__== '__main__':
    from server import app
    connect_to_db(app)

secrets_dict = json.loads(open('data/secrets.json').read())
twilio_sid = secrets_dict["TWILIO_ACCOUNT_SID"]
auth_token = secrets_dict["TWILIO_AUTH_TOKEN"]
message_service_sid = secrets_dict["MESSAGING_SERVICE_SID"]
verify_service_sid = secrets_dict["VERIFY_SERVICE_SID"]

account_sid = twilio_sid
auth_token = auth_token
client = Client(account_sid, auth_token)

twilio_number = '+15103300507'

def send_token(phone):
    """ Start a verification, send verification token """
    verification = client.verify \
                        .services(verify_service_sid) \
                        .verifications \
                        .create(to=phone, channel='sms')
    print(verification.status)


def check_verification(phone, code):
    """ Check a verification (validate) """
    verification_check = client.verify \
                            .services(verify_service_sid) \
                            .verification_checks \
                            .create(to=phone, code=code)
    print(verification_check.status)
    return verification_check.status

def confirm_sub(phone):

    user = get_user_by_phone(phone)
    print(user)

    quote = f'{user.name} is now subscribed to Spark Your Day!'
    message = client.messages.create(to=phone,
                                    from_=twilio_number,
                                    body=quote)
    print(message)


def confirm_unsub(phone):
    
    user = get_user_by_phone(phone)
    print(user)

    quote = f'{user.name} has been unsubscribed from Spark Your Day. Come back any time!'
    message = client.messages.create(to=phone,
                                    # messaging_service_sid=message_service_sid,
                                    from_=twilio_number,
                                    body=quote)
    print(message)