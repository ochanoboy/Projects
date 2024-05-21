account = input("account")
password = input("password")

password_len = len(password)
secure_pass = '*' * password_len

print(f'{account}, your password {secure_pass} is {password_len} letters long')