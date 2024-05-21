with open('test.txt') as my_file:  #no need to close the file
  print(my_file.readlines())

with open('test.txt', mode='r+') as my_file:  #read/write mode (writing to the beginnging of the file
  text = my_file.write(
    'hey it\'s me!')
print(text)
  
with open('test.txt', mode='w') as my_file:  #rewrite mode (rewrite content of the file
  text = my_file.write('hey it\'s me!')
print(text)
  
with open('test.txt', mode='a') as my_file:  #write mode (writing to the end of the file
  text = my_file.write('hey it\'s me!')
  print(text)