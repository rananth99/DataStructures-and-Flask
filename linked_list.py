# structure of a node
class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

# wrapper class for Linked List
class LinkedList:
    # declaring the head and last node of the linked list
    def __init__(self):
        self.head = None
        self.last_node = None
    
    # get_user_by function retrieves a particular user based on the user id by traversing through the linked list
    def get_user_by_id(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data
            node = node.next_node
        return None

    # to_list function appends all the contents of the linked list to a list
    def to_list(self):
        l = []
        if self.head is None:
            return l
        else:
            node = self.head
            while node is not None:
                l.append(node.data)
                node = node.next_node
            return l

    # print_ll function prints the linked list
    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f"{str(node.data)} -> "
            node = node.next_node
        ll_string += " None "
        print(ll_string)

    # insert_at_beginning function inserts the data at the beginning of the linked list and modifies the head and last node
    def insert_at_beginning(self,data):
        if self.head is None:
            self.head = Node(data,None)
            self.last_node = self.head
        else:
            new_node = Node(data,self.head)
            self.head = new_node
    
    # insert_at_end function inserts the data at the end of the linked list and modifies the last node
    def insert_at_end(self,data):
        if self.head is None:
            self.insert_at_beginning(data)
        else:
            self.last_node.next_node = Node(data,None)
            self.last_node = self.last_node.next_node