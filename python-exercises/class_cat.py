class Cat:
  species = 'mammal'
  def __init__(self, name, age):
      self.name = name
      self.age = age
cat1 = (Cat("Kika", 2))
cat2 = (Cat("Kika1", 4))
cat3 = (Cat("Kika2", 9999))

print(cat1.age)
def the_old():
  return max([cat1.age, cat2.age, cat3.age])
print(f"The oldest cat is {the_old()} years old.")

# 2 Create a function that finds the oldest cat.
def oldest_cat(*args):
    return max(args)
# 3 Print out: "The oldest cat is x years old.".

print(f'Oldest Cat is {oldest_cat(cat1.age, cat2.age, cat3.age)} years old.')