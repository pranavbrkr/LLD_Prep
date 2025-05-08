from abc import ABC, abstractmethod

# Strategy interface
class Strategy(ABC):
  @abstractmethod
  def executeStrategy(self):
    pass

# Create strategy interface
class ConcreteStrategyA(Strategy):
  def executeStrategy(self):
    return "Executing Strategy A"

class ConcreteStrategyB(Strategy):
  def executeStrategy(self):
    return "Executing Strategy B"

# Context
class Context:
  def __init__(self, strategy):
    self._strategy = strategy
  
  def setStrategy(self, strategy):
    self._strategy = strategy
  
  def executeStrategy(self):
    return self._strategy.executeStrategy()


if __name__ == "__main__":
  strategy_a = ConcreteStrategyA()
  strategy_b = ConcreteStrategyB()

  context = Context(strategy_a)
  print(context.executeStrategy())

  context.setStrategy(strategy_b)
  print(context.executeStrategy())