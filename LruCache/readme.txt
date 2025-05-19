Use Doubly Linked List to track which is the most recent and lest recent node
Right pointer tracks the most recently used
Left tracks the least recently used
Maintain a map of key -> Node(key, val)

Define Node class, with attributes key, val, next and previos

Define LRUCache class with attributes capacity, cache = {}, lru pointer (dummy left) and mru pointer (dummy right)

Define utility functions
1. remove(node): remove the prev and next references of its previous and next nodes
2. insert(node): insert the node to previous of mru

PUT(key, val)
if key is in cache, remove the corresponding node
Put new node in the cache location
Insert the node in the list
if capacity exceeded
remove lru.next node and delete the corresponding cache entry


GET(key)
if key in cache
remove the corresponding node
insert the same node again and return the val
else return -1