from abc import ABC, abstractmethod
from random import randrange
from typing import List

class Subject(ABC):
  @abstractmethod
  def attach(self, observer):
    pass

  @abstractmethod
  def detach(self, observer):
    pass

  @abstractmethod
  def notify(self):
    pass

class ConcreteSubject(Subject):
  _state: int = None
  _observers = []

  def attach(self, observer):
    print("Subject: Attached an observer")
    self._observers.append(observer)
  
  def detach(self, observer):
    self._observers.remove(observer)
  
  def notify(self):
    print("Subject: Notifying observers...")
    for observer in self._observers:
      observer.update(self)
  
  def somBusinessLogic(self):
    print("Something imp")
    self._state = randrange(0, 10)
    print(f"Subject: My state has just changed to: {self._state}")
    self.notify()

class Observer(ABC):
  @abstractmethod
  def update(self, subject: Subject):
    pass

class ConcreteObserverA(Observer):
  def update(self, subject: Subject):
    if subject._state < 3:
      print("ConcreteObserverA: Reacted to the event")

class ConcreteObserverB(Observer):
  def update(self, subject: Subject):
    if subject._state == 0 or subject._state >= 2:
      print("ConcreteObserverB: Reacted to the event")

if __name__ == "__main__":

  subject = ConcreteSubject()

  observer_a = ConcreteObserverA()
  subject.attach(observer_a)

  observer_b = ConcreteObserverB()
  subject.attach(observer_b)

  subject.somBusinessLogic()
  subject.somBusinessLogic()

  subject.detach(observer_a)
  subject.somBusinessLogic()