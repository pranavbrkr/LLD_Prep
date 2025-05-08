import threading

class Singleton:
  _instance = None
  _lock = threading.Lock()

  def __init__(self):
    if not hasattr(self, '_initialized'):
      self._count = 0
      self._initialized = True
  
  def addCount(self):
    self._count += 1

  def getCount(self):
    return self._count

  def __new__(cls):
    with cls._lock:
      if cls._instance is None:
        cls._instance = super(Singleton, cls).__new__(cls)
    return cls._instance
  
if __name__ == "__main__":
  count = Singleton()
  print(count.getCount())
  print(count.addCount())
  count2 = Singleton()
  print(count2.getCount())