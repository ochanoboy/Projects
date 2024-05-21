from cryptography.fernet import Fernet
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import sys

# read from file func
def read_secrets(filename, key):
    with open(filename, 'rb') as file:
        encrypted_data = file.read().splitlines()
        f = Fernet(key)
        decrypted_data = [f.decrypt(line).decode() for line in encrypted_data]
        return decrypted_data[0], decrypted_data[1]

# key
key = b'duzgxnD9iKkK_iY_g0F8I8go0P0XfsTD9EouPeAWPD8='

# get encrypt vars from file
account, pswd = read_secrets('secrets.txt', key)

###################################################################

html = Template(Path('index.html').read_text())

# email block
email = EmailMessage()
email['from'] = 'tech-team@gmail.kika'
to_emails = sys.argv[1].split(',') #first arg (one or more email addresses (kika1@gmail.com,kika2@gmail.com))
email['to'] = to_emails
email['subject'] = str(sys.argv[2])

email.set_content(html.substitute({'name': 'Andrew'}), 'html')

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()  # init smtp
    smtp.starttls()  # secure the connection
    smtp.login(account, pswd)
    smtp.send_message(email)
    print('message sent')
