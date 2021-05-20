# structure of a node
class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

# class to define the structure of the data 
class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value

# wrapper class for Hash Table
class HashTable:
    # declaring the table size and the hash table of the desired size
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size

    # custom_hash function to generate a customized hash value within the size of the hash table for the given key
    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        return hash_value

    # add_key_value function to insert the key and value to the created hash table based on the custom hash value
    def add_key_value(self, key, value):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:
            node = self.hash_table[hashed_key]
            while node.next_node is not None:
                node = node.next_node
            
            node.next_node = Node(Data(key, value), None)
    
    # get_value function to fetch the value corresponding to the desired key sent as parameter
    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_node is None:
                return node.data.value
            while node.next_node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node

            if key == node.data.key:
                return node.data.value
        return None

    # print_table function to print the hash table
    def print_table(self):
        print(" { ")
        for i, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                            str(node.data.key) + ":" + str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (
                            str(node.data.key) + ":" + str(node.data.value) + " --> None "
                        )
                    print(f"    [{i}]   {llist_string} ")
                else:
                    print(f"    [{i}]   {val.data.key}:{val.data.value} ")
            else:
                print(f"    [{i}]   {val} ")
        print(" } ")
