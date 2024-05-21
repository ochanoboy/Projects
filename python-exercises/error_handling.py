while True:
  try:
      age = int(input('what is your age?'))
      print(age)
      10/age
  except ValueError:
      print('please enter a number')
      continue
  except ZeroDivisionError:
      print('please enter age higher than 0')
  else:
      print('thank you')
      break
  finally:
      print('ok, i am finally done') #no matter what funally will run
  print('can u hear me?')
  