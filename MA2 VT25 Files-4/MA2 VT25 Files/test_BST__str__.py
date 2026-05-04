# https://docs.python.org/3/library/unittest.html
"""
Unittests for the binary search tree methods
"""

import unittest

from bst import *
from linked_list import *


class Test(unittest.TestCase):

    def test___str__(self):
        bst = BST()
        self.assertEqual(str(bst), '<>')
        bst.insert(3)
        self.assertEqual(str(bst), '<3>')
        bst.insert(2)
        self.assertEqual(str(bst), '<2, 3>')
        bst.insert(4)
        self.assertEqual(str(bst), '<2, 3, 4>')

if __name__ == "__main__":
    unittest.main()


