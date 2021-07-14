import csv
import os
import smtplib
import csv
from email.message import EmailMessage
from configuration import ScriptVars

def send_batch_email(subject, body, attachments=None):
    recipients = []
    config_vars = ScriptVars()
    with open('recipients.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if '@' in row[0]:
                recipients.append(row[0])
                
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['Body'] = body
    # msg.set_content(body)
    msg['From'] = config_vars.EMAIL_ADDRESS 
    msg['To']   = ', '.join(recipients)

    #Open csv file as 'rb' for attachments
    if attachments != None:
        for attachment in attachments:
            with open(attachment, 'rb'):
                pass

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(config_vars.EMAIL_ADDRESS, config_vars.EMAIL_PASS)
        smtp.send_message(msg)
