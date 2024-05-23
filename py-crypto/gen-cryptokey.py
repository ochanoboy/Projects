from cryptography.fernet import Fernet
import sys

#gen key
key = Fernet.generate_key()
print(key.decode())  #output

#data to encrypt
f = Fernet(key)
account = sys.argv[1].encode()
pswd = sys.argv[2].encode()

#encrypt
encrypted_account = f.encrypt(account)
encrypted_pswd = f.encrypt(pswd)

#create encrypt data file
with open('secrets.txt', 'wb') as file:
    file.write(encrypted_account + b'\n')
    file.write(encrypted_pswd + b'\n')
    print('encrypting data created!')




