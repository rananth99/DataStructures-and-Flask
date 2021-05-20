# structure of a node
class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

# wrapper class for Queue
class Queue:
    # declaring the head and tail of a queue
    def __init__(self):
        self.head = None
        self.tail = None
    
    # enqueue function to insert into the queue and modify the head and tail
    def enqueue(self, data):
        if self.head is None and self.tail is None:
            self.head = self.tail = Node(data, None)
            return
        else:
            self.tail.next_node = Node(data, None)
            self.tail = self.tail.next_node
            return

    # dequeue function to remove from the queue and modify the head and tail
    def dequeue(self):
        if self.head is None:
            return
        else:
            removed_node = self.head
            self.head = self.head.next_node
            if self.head is None:
                self.tail = None
        return removed_node
