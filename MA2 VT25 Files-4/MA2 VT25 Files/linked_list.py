""" linked_list.py

Student: Hugo Lovmar
Mail: hlovmar@gmail.com
Reviewed by: Filip
Date reviewed: 2026-04-22
"""
class Person: #for Ex7
    def __init__(self, name, pnr):
        self.name = name
        self.pnr = pnr

    def __lt__(self, other):
        return self.pnr < other.pnr

    def __le__(self, other):
        return self.pnr <= other.pnr

    def __eq__(self, other):
        return self.pnr == other.pnr
    
    def __str__(self):
        return f"{self.name}:{self.pnr}"


class LinkedList:

    class Node:
        def __init__(self, data, succ):
            self.data = data
            self.succ = succ

    def __init__(self):
        self.first = None

    def __iter__(self):            # Discussed in the section on iterators and generators
        current = self.first
        while current:
            yield current.data
            current = current.succ

    def __in__(self, x):           # Discussed in the section on operator overloading
        for d in self:
            if d == x:
                return True
            elif x < d:
                return False
        return False

    def insert(self, x):
        if self.first is None or x <= self.first.data:
            self.first = self.Node(x, self.first)
        else:
            f = self.first
            while f.succ and x > f.succ.data:
                f = f.succ
            f.succ = self.Node(x, f.succ)

    def print(self):
        print('(', end='')
        f = self.first
        while f:
            print(f.data, end='')
            f = f.succ
            if f:
                print(', ', end='')
        print(')')

    # To be implemented

    def length(self):          #   Ex1
        if self.first is None:
            return 0
        else:
            count = 0
            f = self.first
            while f:
                count += 1
                f = f.succ
            return count
        

    def mean(self):               
        pass

    def remove_last(self):       # Ex2
        if self.first is None:
            raise ValueError("Empty list")

        if self.first.succ is None:
            data = self.first.data
            self.first = None
            return data

        prev = self.first
        curr = self.first.succ

        while curr.succ:
            prev = curr
            curr = curr.succ

        prev.succ = None
        return curr.data


    def remove(self, x):         # Ex3
        if self.first is None:
            return False
        
        if self.first.data == x:
            self.first = self.first.succ
            return True
        
        prev = self.first
        curr = self.first.succ

        while curr:
            if curr.data == x:
                prev.succ = curr.succ
                return True
            
            prev = curr
            curr = curr.succ

        return False


    def to_list(self):            # Ex4

        def _to_list(node):
            if node is None:
                return []
            
            else:
                return [node.data] + _to_list(node.succ)
            
        return _to_list(self.first)
    

    def __str__(self):            # Ex5
        values = [str(x) for x in self]

        return '(' + ', '.join(values) + ')'

    def copy(self):
        result = LinkedList()

        for x in self:
            result.insert(x)

        return result
    
    ''' Complexity for this implementation: 
    O(n^2)
    '''

    def copy(self):               # Ex6, Should be more efficient
        result = LinkedList()

        if self.first is None:
            return result
        
        result.first = self.Node(self.first.data, None)

        curr_src = self.first.succ
        curr_dst = result.first

        while curr_src:
            new_node = LinkedList.Node(curr_src.data, None)
            curr_dst.succ = new_node
            curr_dst = new_node
            curr_src = curr_src.succ

        return result                      
    
    ''' Complexity for this implementation:
    O(n)
    '''


def main():
    lst = LinkedList()
    for x in [1, 1, 1, 2, 3, 3, 2, 1, 9, 7]:
        lst.insert(x)
    lst.print()

    plist = LinkedList() # Ex7
    p = Person("Hugo", "2003")
    q = Person("Oguh", "3002")
    
    plist.insert(p)
    plist.insert(q)

    print (plist)

    # Test code:


if __name__ == '__main__':
    main()
