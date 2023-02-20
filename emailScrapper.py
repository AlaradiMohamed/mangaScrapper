import smtplib
import psword
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def sendEmail(emailsList, files, messageBody = ''):
    # Define the email sender, recipient, subject, and body
    from_address = 'animeScrapper@gmail.com'
    to_address = emailsList
    subject = 'Manga Scrapping Results'
    body = messageBody

    # Create a message object and set its attributes
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    # add the body of the email
    msg.attach(MIMEText(body, 'plain'))


    # loop through the file names and add each one as an attachment to the email
    for filename in files:
        with open(filename, 'rb') as attachment:
            # add the PDF as application/octet-stream
            # email clients will treat this as a PDF attachment
            attachment_part = MIMEApplication(attachment.read(), _subtype="pdf")
            attachment_part.add_header('Content-Disposition','attachment',filename=filename.split('/')[-1])
            msg.attach(attachment_part)

    # create the SMTP server object and send the message
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = psword.smtp_name
    smtp_password = psword.smtp_paswrd
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(from_address, to_address, msg.as_string())
    server.quit()
