# structure of a node
class Node:
    def __init__(self, data, next_node):
        self.data = data
        self.next_node = next_node

# wrapper class for Stack
class Stack:
    # declaring the top of the stack
    def __init__(self):
        self.top = None
    
    # peak function to find the top element of the stack
    def peak(self):
        return self.top

    # push function to insert the element to the top of the stack and reasign the top of the stack
    def push(self, data):
        next_node = self.top
        new_top = Node(data, next_node)
        self.top = new_top 

    # pop function to delete the top element of the stack and reassign the top of the stack
    def pop(self):
        if self.top is None:
            return None
        else:
            removed_node = self.top
            self.top = self.top.next_node
            return removed_node
