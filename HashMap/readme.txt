For hash functions, we use strategy pattern
With HashFunction interface and the classes which implement this interface with their specific hash mechanisms


We have different hash buckets.
In this bucket will be the singly linked list.
We will replace the value for the corresponding node if the key exists or else we will append the new node at the start and reassign the head to it
Bucket class will have insert(key, value), find(key) and delete(key)

Define HashNode class that holds  key, value and next pointer

Now the main Hashmap class
This will have following attributes
capacity: total capacity as of now
size: to track current size
load_factor_threshold: which helps us determine when to resize
hash_function
buckets array: which is the Bucket() object in range(0, self.capacity)

And following behaviors
1. get index: get the bucket by calling hash_function.hash()

2. put: this first calls get index. Then on that bucket index, if key not found using the find function, increment the size. Insert into bucket.
if size/capacity > load_factor_threshold, call resize()

3. get: calls get index and retuns bucket[index].find()

4. remove: deleted the key from the bucket. If something is removed, decrement size

5. resize: Firstly, store old buckets into a variable. Then double the capacity and declare empty buckets for the range (0, capacity)
Now for each bucket in old bucket:
assign node to head and put all the nodes in that bucket
assign the size to old size