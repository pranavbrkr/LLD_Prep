from abc import ABC, abstractmethod

# Component
class Character(ABC):
  @abstractmethod
  def getDescription(self):
    pass

  def getDamage(self):
    pass

# Concrete component
class BasicCharacter(Character):
  def getDescription(self):
    return "Basic Character"

  def getDamage(self):
    return 10

# Decorator
class CharacterDecorator(Character, ABC):
  def __init__(self, character):
    self._character = character
  
  @abstractmethod
  def getDescription(self):
    pass

  @abstractmethod
  def getDamage(self):
    pass


# Concrete decorators
class DoubleDamageDecorator(CharacterDecorator):
  def getDescription(self):
    return self._character.getDescription() + " with Double Damage"
  
  def getDamage(self):
    return self._character.getDamage() * 2

class FireballDecorator(CharacterDecorator):
  def getDescription(self):
    return self._character.getDescription() + " with Fireball"
  
  def getDamage(self):
    return self._character.getDamage() + 20

class InvisibilityDecorator(CharacterDecorator):
  def getDescription(self):
    return self._character.getDescription() + " with Invisibility"
  
  def getDamage(self):
    return self._character.getDamage()
  

# Client code
if __name__ == "__main__":
  character = BasicCharacter()
  print(character.getDescription())
  print(character.getDamage())

  double_damage_decorator = DoubleDamageDecorator(character)
  fireball_decorator = FireballDecorator(character)
  invisibility_decorator = InvisibilityDecorator(character)

  print(double_damage_decorator.getDescription())
  print(double_damage_decorator.getDamage())

  print(fireball_decorator.getDescription())
  print(fireball_decorator.getDamage())

  print(invisibility_decorator.getDescription())
  print(invisibility_decorator.getDamage())

  double_fireball_character = DoubleDamageDecorator(FireballDecorator(character))
  print(double_fireball_character.getDescription())
  print(double_fireball_character.getDamage())

  invisibility_double_fireball_character = InvisibilityDecorator(DoubleDamageDecorator(FireballDecorator(character)))
  print(invisibility_double_fireball_character.getDescription())
  print(invisibility_double_fireball_character.getDamage())