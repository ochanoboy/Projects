class PlayerCharacter:
  def __init__(self, name, age):  #constructor or init method
    self.name = name #attributes
    self.age = age
  def run(self):
    print('run')
    return 'done'

player1 = PlayerCharacter('Kika', 44)
player2 = PlayerCharacter('Rika', 21)
player2.attack = 50
print(player1) #outputs the place in mem where class is stored
print(player2) #player1 and player2 objects stored in different places in mem
print(player1.name)
print(player2.name)
print(player1.age) #hey i want to access the attribute age
print(player2.age)
print(player1.run())

print(player2.attack)