""" bst.py

Student: Hugo Lovmar
Mail: hlovmar@gmail.com
Reviewed by: Filip
Date reviewed: 2026-04-22
"""


from linked_list import LinkedList


class BST:

    class Node:
        def __init__(self, key, left=None, right=None):
            self.key = key
            self.left = left
            self.right = right

        def __iter__(self):     # Discussed in the text on generators
            if self.left:
                yield from self.left
            yield self.key
            if self.right:
                yield from self.right

    def __init__(self, root=None):
        self.root = root

    def __iter__(self):         # Dicussed in the text on generators
        if self.root:
            yield from self.root

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, r, key):
        if r is None:
            return self.Node(key)
        elif key < r.key:
            r.left = self._insert(r.left, key)
        elif key > r.key:
            r.right = self._insert(r.right, key)
        else:
            pass  # Already there
        return r

    def print(self):
        self._print(self.root)

    def _print(self, r):
        if r:
            self._print(r.left)
            print(r.key, end=' ')
            self._print(r.right)

    def contains_given(self, k): # given function
        n = self.root
        while n and n.key != k:
            if k < n.key:
                n = n.left
            else:
                n = n.right
        return n is not None

    # def contains(self, k) # Ex8: write recursive contains

    def contains(self, k):
        return self._contains(self.root, k)
    
    def _contains(self, r, k):
        if r is None:
            return False
        elif k < r.key:
            return self._contains(r.left, k)
        elif k > r.key:
            return self._contains(r.right, k)
        else:
            return True
    
    def size(self):
        return self._size(self.root)

    def _size(self, r):
        if r is None:
            return 0
        else:
            return 1 + self._size(r.left) + self._size(r.right)

#
#   Methods to be completed
#

    def height(self):                 #        Ex9     
        if self.root is None:
            return 0
        else:
            return self._height(self.root)
        
    def _height(self, r):
        if r is None:
            return 0
        else:
            return 1 + max(self._height(r.left), self._height(r.right))

    def __str__(self):                #     Ex10       
        return '<' + ', '.join(str(k) for k in self) + '>'

    def to_list(self):
        return [x for x in self]  # Ex11
    
    """
Complexity of to_list: Theta(n), every node is visited once.
"""

    def to_LinkedList(self):    #     Ex12
        result = LinkedList()
        last = None

        for key in self:
            new_node = LinkedList.Node(key, None)
            if last is None:
                result.first = new_node
            else:
                last.succ = new_node
            last = new_node
        
        return result 
    """
Complexity of _LinkedList: theta(n)
"""
    def remove(self, key): #
        self.root = self._remove(self.root, key)

    def _remove(self, r, k):                      # Ex13
        if r is None:
            return None
        elif k < r.key:
            r.left = self._remove(r.left, k)
        elif k > r.key:
            r.right = self._remove(r.right, k)
        else:  # This is the key to be removed
            if r.left is None:     # Easy case
                return r.right
            elif r.right is None:  # Also easy case
                return r.left
            else:  # This is the tricky case.
                successor = r.right
                # Find the smallest key in the right subtree
                while successor.left:
                    successor = successor.left
                # Put that key in this node
                r.key = successor.key
                # Remove that key from the right subtree
                r.right = self._remove(r.right, successor.key)    
        return r  # Remember this! It applies to some of the cases above


def main():
    t = BST()
    for x in [4, 1, 3, 6, 7, 1, 1, 5, 8]:
        t.insert(x)
    t.print()
    print()

    print('size  : ', t.size())
    for k in [0, 1, 2, 5, 9]:
        print(f"contains({k}): {t.contains(k)}")


if __name__ == "__main__":
    main()


"""
Ex14: What is the generator good for?
==============================

1. computing size? Works but no benefit compared to the recursive _size
2. computing height? Not good
3. contains? Wasteful compeared tor ecursive contains
4. insert? Need to navigate tree strucutre. Not good
5. remove? Same as above

The generator is good for to_list, to_linkedlist, and __str__, where we need to visit all nodes in the tree. It is not good for size, height, contains, insert, and remove, where we need to navigate the tree structure and do not need to visit all nodes.

Exercise 14 in the document: Complexity of search:
1. worst case: theta(n) (when the tree is a chain)
2. Average case: theta(log n) (when the tree is balanced)
3. Unsuccessful search: theta(n) (when the tree is a chain and the key is not in the tree) and theta(log n) (when the tree is balanced and the key is not in the tree).

The BST performance is determined by the height of the tree. 
"""
