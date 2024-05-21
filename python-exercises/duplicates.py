list = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
duplicates = []
for value in list:
  if list.count(value) > 1 and value not in duplicates:
    duplicates.append(value)
print(duplicates)