from twilio.rest import Client
from flight_data import FlightData
import os

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACC_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_ATH_TOKEN")
DST_TEL_NUMBER = YOUR DESTINATION NUMBER
TWILIO_DISPATCH_NUMBER = YOUR TWILIO DISPATCH NUMBER


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.twilio_account_sid = TWILIO_ACCOUNT_SID
        self.twilio_auth_token = TWILIO_AUTH_TOKEN
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)

    def send_sms(self, message_text):
        """Sends sms via twilio"""
        message = self.client.messages.create(
                body=message_text,
                from_=TWILIO_DISPATCH_NUMBER,
                to=DST_TEL_NUMBER
        )
        print("Message: ",message.status)
        print(f"This message was send:\n{message_text}")
