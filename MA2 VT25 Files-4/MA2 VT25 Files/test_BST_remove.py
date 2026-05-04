"""
Unittests for the binary search tree methods
"""

import unittest

from bst import *
from linked_list import *


class Test(unittest.TestCase):

    def test_remove(self):
        
        def is_bst(node):
            if node is None:
                return True
            elif node.left and node.left.key > node.key:
                return False
            elif node.right and node.right.key < node.key:
                return False
            else:
                return is_bst(node.left) and is_bst(node.right)

        print('\nTests BST remove')
        bst = BST()
        lst = [10, 5, 3, 8, 1, 4, 6, 9, 2, 7]
        print('Insert order: ', lst)        
        for x in lst:   
            bst.insert(x)
        print(f'Initial tree : {bst}')
        
        bst.remove(2)
        print(f'After remove 2: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 2: {bst}')
        self.assertEqual(str(bst), '<1, 3, 4, 5, 6, 7, 8, 9, 10>')
        bst.remove(1)
        print(f'After remove 1: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 1: {bst}')
        self.assertEqual(str(bst), '<3, 4, 5, 6, 7, 8, 9, 10>')
        bst.remove(4)
        print(f'After remove 4: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 4: {bst}')
        self.assertEqual(str(bst), '<3, 5, 6, 7, 8, 9, 10>')
        bst.remove(6)
        print(f'After remove 6: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 6: {bst}')
        self.assertEqual(str(bst), '<3, 5, 7, 8, 9, 10>')
        bst.remove(2)
        print(f'After remove 2: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 2: {bst}')
        self.assertEqual(str(bst), '<3, 5, 7, 8, 9, 10>')
        bst.remove(5)
        print(f'After remove 5: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 5: {bst}')
        self.assertEqual(str(bst), '<3, 7, 8, 9, 10>')
        bst.remove(3)
        print(f'After remove 3: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 3: {bst}')
        self.assertEqual(str(bst), '<7, 8, 9, 10>')
        bst.remove(7)
        print(f'After remove 7: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 7: {bst}')
        self.assertEqual(str(bst), '<8, 9, 10>')
        bst.remove(8)
        print(f'After remove 8: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 8: {bst}')
        self.assertEqual(str(bst), '<9, 10>')
        bst.remove(9)
        print(f'After remove 9: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 8: {bst}')
        self.assertEqual(str(bst), '<10>')
        bst.remove(10)
        print(f'After remove 10: {bst}')
        self.assertTrue(is_bst(bst.root), f'Not a BST after remove 10: {bst}')
        self.assertEqual(str(bst), '<>')


if __name__ == "__main__":
    unittest.main()
