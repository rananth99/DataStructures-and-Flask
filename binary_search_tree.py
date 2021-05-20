# structure of a node
class Node:
    def __init__(self, data=None):
        self.data = data 
        self.left = None
        self.right = None

# wrapper class for Binary Search Tree
class BinarySearchTree:
    # declaring the root of the tree
    def __init__(self):
        self.root = None

    # _insert_recursive function is a private function used by insert function
    # this recursively traverses the binary search tree based on the value to be inserted
    def _insert_recursive(self, data, node):
        if data["id"] < node.data["id"]:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(data, node.left)
        elif data["id"] > node.data["id"]:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(data, node.right)
        else:
            return

    # insert function inserts the value by calling _insert_recursive function
    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert_recursive(data, self.root)

    # _search_recursive function is a private function used by search function
    # this recursively traverses the binary search tree based on the value to be retrieved
    def _search_recursive(self, blog_post_id, node):
        if blog_post_id == node.data["id"]:
            return node.data

        if blog_post_id < node.data["id"] and node.left is not None:
            if blog_post_id == node.left.data["id"]:
                return node.left.data
            return self._search_recursive(blog_post_id, node.left)

        if blog_post_id > node.data["id"] and node.right is not None:
            if blog_post_id == node.right.data["id"]:
                return node.right.data
            return self._search_recursive(blog_post_id, node.right)

        return False

    # search function calls the _search_recursive function to search for the desired value
    def search(self, blog_post_id):
        post_id = int(blog_post_id)
        if self.root is None:
            return False
        else:
            return self._search_recursive(post_id, self.root)
