some_lst = ['a', 'b', 'c', 'b', 'd', 'm', 'n', 'n']
duplicates = list(set([dupl for dupl in some_lst if some_lst.count(dupl) > 1]))
print(duplicates)