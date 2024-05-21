li = [1,2,5,7,9,11,77,1,6,99,10000]
def highest_ever(li):
  total = 0
  for index in li:
    if total < index:
     total = index
    else:
      continue
  return total
print(highest_ever(li))