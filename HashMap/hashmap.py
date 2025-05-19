from abc import ABC, abstractmethod

class IHashFunction(ABC):
  @abstractmethod
  def hash(self, key, capacity):
    pass

class DefaultHashFunction(IHashFunction):
  def hash(self, key, capacity):
    return hash(key) % capacity
  
class HashNode:
  def __init__(self, key, value):
    self.key = key
    self.value = value
  
class Bucket:
  def __init__(self):
    self.head = None

  def insert(self, key, value):
    node = self.head
    while node:
      if node.key == key:
        node.val = value
        return
      node = node.next
    new_node = HashNode(key, value)
    new_node.next = self.head
    self.head = new_node
  
  def find(self, key):
    node = self.head
    while node:
      if node.key == key:
        return node
      node = node.next
    return None
  
  def delete(self, key):
    prev, node = None, self.head
    while node:
      if node.key == key:
        if prev:
          prev.next = node.next
        else:
          self.head = node.next
        return True
      prev = node
      node = node.next
    return False
  
class Hashmap:
  def __init__(self, capacity = 8, threshold = 0.75, hash_function = None):
    self.capacity = capacity
    self.threshold = threshold
    self.size = 0
    self.buckets = [Bucket() for _ in range(self.capacity)]
    self.hash_function = hash_function or DefaultHashFunction()
  
  def _getIndex(self, key):
    return self.hash_function.hash(key, self.capacity)

  def put(self, key, value):
    index = self._getIndex(key)
    if not self.buckets[index].find(key):
      self.size += 1
    self.buckets[index].insert(key, value)

    if (self.size / self.capacity) > self.threshold:
      self._resize()

  def get(self, key):
    index = self._getIndex(key)
    return self.buckets[index].find(key)

  def remove(self, key):
    index = self._getIndex(key)
    removed = self.buckets[index].delete(key)
    if removed:
      self.size -= 1
  
  def _resize(self):
    print(f"Resizing from {self.capacity} to {self.capacity * 2}")
    old_size = self.size
    old_buckets = self.buckets
    self.capacity *= 2
    self.buckets = [Bucket() for _ in range(self.capacity)]
    self.size = 0

    for bucket in old_buckets:
      node = self.head
      while node:
        self.put(node.key, node.value)
        node = node.next
    self.size = old_size
  
  def __str__(self):
    result = []

    for i, bucket in enumerate(self.buckets):
      node = bucket.head
      items = []
      while node:
        items.append(f"({node.key}, {node.value})")
        node = node.next
      result.append(f"Bucket {i}:" + "->".join(items))
    return "\n".join(result)

if __name__ == "__main__":
  hm = Hashmap()
  hm.put("apple", 10)
  hm.put("banana", 20)
  hm.put("orange", 30)
  hm.put("banana", 25)
  hm.remove("apple")

  print(hm.get("banana"))
  print(hm.get("apple"))
  print(hm)