from threading import Lock

class Node:
  def __init__(self, key, val):
    self.key = key
    self.val = val
    self.prev = self.next = None

class LRU:
  _instance = None
  _lock = Lock()

  def __new__(cls, capacity):
    with cls._lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
        cls._instance._init_once(capacity)
      return cls._instance

  def _init_once(self, capacity):
    if hasattr(self, "_initialized"):
      return
    self.capacity = capacity
    self.cache = {}
    self.mru, self.lru = Node(-1, -1), Node(-1, -1)
    self.lru.next = self.mru
    self.mru.prev = self.lru
    self._initialized = True

  def insert(self, node):
    prv = self.mru.prev
    prv.next = node
    self.mru.prev = node
    node.prev = prv
    node.next = self.mru
  
  def remove(self, node: Node):
    prv, nxt = node.prev, node.next
    prv.next = nxt
    nxt.prev = prv
  
  def put(self, key, val):
    with self._lock:
      if key in self.cache:
        self.remove(self.cache[key])
      self.cache[key] = Node(key, val)
      self.insert(self.cache[key])

      if self.capacity < len(self.cache):
        lru = self.lru.next
        self.remove(lru)
        del self.cache[lru.key]
  
  def get(self, key):
    with self._lock:
      if key in self.cache:
        self.remove(self.cache[key])
        self.insert(self.cache[key])
        return self.cache[key].val
      return -1
  
if __name__ == "__main__":
  lru = LRU(2)
  lru.put(1, 'A')
  lru.put(2, 'B')
  print(lru.get(1))  # A
  lru.put(3, 'C')    # Evict key 2
  print(lru.get(2))  # -1
  print(lru.get(3))  # C
