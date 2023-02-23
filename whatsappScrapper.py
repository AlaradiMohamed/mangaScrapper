# %%
import psword
from twilio.rest import Client
from datetime import datetime, timedelta
from urllib.parse import urlparse

# %%
def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# %%
def getURLs():
    account_sid = psword.twilio_sid
    auth_token = psword.twilio_token
    client = Client(account_sid, auth_token)

    today = datetime.today()
    before_yesterday = today - timedelta(days=2)
    urls = []

    messages = client.messages.list(
        to=f'whatsapp:{psword.twilio_number}',
        date_sent_after=before_yesterday.date(),
        date_sent_before=today.date()
    )

    for message in messages:
        if is_url(message.body):
            urls.append(message.body)
            
    return urls


# %%
def sendWhatsappMsg(phoneNumber, messageBody):
    account_sid = psword.twilio_sid
    auth_token = psword.twilio_token

    client = Client(account_sid, auth_token)

    to_number = f'whatsapp:{phoneNumber}'

    message = client.messages.create(
        from_=f'whatsapp:{psword.twilio_number}',
        body=messageBody,
        to=to_number
    )
    return message


