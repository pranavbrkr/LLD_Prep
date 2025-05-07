from abc import ABC, abstractmethod

class Product(ABC):
  @abstractmethod
  def operation(self) -> str:
    pass

class ConcreteProduct1(Product):
  def operation(self) -> str:
    return "{Result of ConcreteProduct1}"

class ConcreteProduct2(Product):
  def operation(self) -> str:
    return "{Result of ConcreteProduct2}"


class Creator(ABC):
  @abstractmethod
  def factoryMethod(self):
    pass

  def someOperation(self) -> str:
    product = self.factoryMethod()
    result = f"Creator: The same creator's code just worked with {product.operation()}"
    return result
  
class ConcreteCreator1(Creator):
  def factoryMethod(self) -> Product:
    return ConcreteProduct1()
  
class ConcreteCreator2(Creator):
  def factoryMethod(self) -> Product:
    return ConcreteProduct2()
  
def clientCode(creator: Creator):
  print(f"Client: No fecking idea who the creator is")
  print(f"{creator.someOperation()}")

print("Launched with ConcreteCreator1")
clientCode(ConcreteCreator1())
print("\n")

print("Launched with ConcreteCreator2")
clientCode(ConcreteCreator2())