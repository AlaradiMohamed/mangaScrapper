# %%
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
    account_sid = 'ACccaf86d24eca0bdb3117be596218388d'
    auth_token = '62912b18e903b8503aafaf94cf11cfc6'
    client = Client(account_sid, auth_token)

    today = datetime.today()
    before_yesterday = today - timedelta(days=2)
    urls = []

    messages = client.messages.list(
        to='whatsapp:+14155238886',
        # date_sent_after=before_yesterday.date(),
        # date_sent_before=today.date()
    )

    for message in messages:
        # print(f"Message ID: {message.sid}")
        # print(f"Date: {message.date_sent}")
        # print(f"Message: {message.body}")
        # print(f"From: {message.from_}")
        # print(f"To: {message.to}")
        if is_url(message.body):
            urls.append(message.body)
            
    return urls


# %%
def sendWhatsappMsg(phoneNumber, messageBody):
    account_sid = 'ACccaf86d24eca0bdb3117be596218388d'
    auth_token = '62912b18e903b8503aafaf94cf11cfc6'

    client = Client(account_sid, auth_token)

    to_number = f'whatsapp:{phoneNumber}'

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=messageBody,
        to=to_number
    )
    return message


