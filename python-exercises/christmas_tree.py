picture = [
  [0,0,0,1,0,0,0],
  [0,0,1,1,1,0,0],
  [0,1,1,1,1,1,0],
  [1,1,1,1,1,1,1],
  [0,0,0,1,0,0,0],
  [0,0,0,1,0,0,0]
 ]
def chris_tree():
  for list in picture:
    print('')
    for item in list:
      if item == 0:
        print(' ', end='')
      else:
        print('*', end='')
chris_tree()