import csv
import os
import smtplib
import csv
from email.message import EmailMessage
#from dotenv import load_dotenv

# load_dotenv()
# print(os.environ['EMAIL_ADDRESS'])
EMAIL_ADDRESS   = ''
EMAIL_PASS      = ''

def send_batch_email(subject, body, attachments=None):
    recipients = []
    with open('recipients.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if '@' in row[0]:
                recipients.append(row[0])
                
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['Body'] = body
    # msg.set_content(body)
    msg['From'] = EMAIL_ADDRESS 
    msg['To']   = ', '.join(recipients)

    #Open csv file as 'rb' for attachments
    if attachments != None:
        for attachment in attachments:
            with open(attachment, 'rb'):
                pass


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)
