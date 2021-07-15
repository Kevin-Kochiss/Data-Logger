import csv
from os import write
from pathlib import Path, PurePath
import re
import smtplib
import csv
from email.message import EmailMessage
from configuration import ScriptVars
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from pathlib import WindowsPath

def send_batch_email(subject=None, body=None, attachments=None):
    config_vars = ScriptVars()
    recipients = get_or_create_recipients(config_vars.RECIPIENTS, config_vars.EMAIL_ADDRESS)

    if not recipients:
        return False
    
    msg = MIMEMultipart()
    if subject != None:
        msg['Subject'] = subject
    elif isinstance(attachments, list):
        msg['Subject'] = PurePath(attachments[0]).name
    elif isinstance(attachments, WindowsPath) or isinstance(attachments, str):
        msg['Subject'] = PurePath(attachments).name.split('.')[0]
    else:
        msg['Subject'] = 'Message from Line 7'
    if body != None:
        msg.attach(MIMEText(body))
    else:
        body = 'Message sent from Data logger on Line 7'
        msg.attach(MIMEText(body))
    msg['From'] = config_vars.EMAIL_ADDRESS 
    msg['To']   = ', '.join(recipients)

    #process attachments if present
    if attachments != None:
        try:
            for attachment in attachments:
                att = prepare_attachment(attachment)
                if att != None:
                    msg.attach(att)
        except:
            att = prepare_attachment(attachments)
            if att != None:
                msg.attach(att)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(config_vars.EMAIL_ADDRESS, config_vars.EMAIL_PASS)
        smtp.send_message(msg)
        smtp.close()
    return True

def prepare_attachment(att):
    if not Path(att).is_file:
        return None
    m_type, encoding = mimetypes.guess_type(att)
    if m_type is None or encoding is not None:
        m_type = "application/octet-stream"
    maintype, subtype = m_type.split("/", 1)
    if maintype == "text":
        with open(att) as file:
            attachment = MIMEText(file.read(), _subtype=subtype)
    elif maintype == "image":
        with open(att, "rb") as file:
            attachment = MIMEImage(file.read(), _subtype=subtype)
    else:
        with open(att, "rb") as file:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment",
    filename=PurePath(att).name)

    return attachment

def get_or_create_recipients(path, default):
    recipients = []
    try:
        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if '@' in row[0]:
                    recipients.append(row[0])
    except:
        with open(path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([default])
    return recipients

def email_errors(error_string):
    if(error_string == 'scanning_rate'):
        error_message = 'An error was detected when attempting to read a file'

def sampling_error(file_path):
    error_msg = 'An error was detected when attempting to read:\n\n{}\n\n'\
        .format(file_path)
    error_msg += 'The sampling rate was not detected on the file.'\
        '\"Sampling\" was not found as a cell item.'\
        'Check to see if this file is the correct type'
    email_errors(error_msg)