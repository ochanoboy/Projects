import re

pattern = re.compile(r"(^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$)") 
string = 'SuperPivo@11234'
password = pattern.search(string)
if password:
  print('valid')
else:
  print('invalid')