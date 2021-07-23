import csv
from os import write
import smtplib
import mimetypes
from pathlib import Path, PurePath
from configuration import ScriptVars
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from pathlib import WindowsPath

def send_batch_email(subject=None, body=None, attachments=None):
    config = ScriptVars()
    recipients = config.get_or_create_recipients()

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
    msg['From'] = config.get_email_address()
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
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(config.get_email_address(), config.get_email_pass())
            smtp.send_message(msg)
            smtp.close()
        clear_error(config.CONFIG_DIR)
        return True
    except:
        if config.can_debug():
            print('Email send failed')  #COuld not connected to the email server, make sure connected to interet
        write_error(config.CONFIG_DIR)
        return False

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

def write_error(config_dir):
    fp = Path.joinpath(config_dir, 'Email_Error.txt')
    if Path(fp).exists():
        return
    try:
        with open(fp, 'w') as f:
            f.write('Email error, failed to connect to server.'
            '\nCheck Internet conection')
    except:
        pass

def clear_error(config_dir):
    fp = Path.joinpath(config_dir, 'Email_Error.txt')
    Path(fp).unlink(True)