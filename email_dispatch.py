import csv
import os
import smtplib
import csv
from email.message import EmailMessage

EMAIL_ADDRESS = ''
EMAIL_PASS = ''

def send_batch_email(subject, body):
    recipients = []
    with open('recipients.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row[0].find('@'):
                recipients.append(row[0])
                
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['Body'] = body
    # msg.set_content(body)
    msg['From'] = EMAIL_ADDRESS 
    msg['To']   = recipients

    #Open csv file as 'rb'


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)
