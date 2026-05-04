# https://docs.python.org/3/library/unittest.html
"""
Unittests for the binary search tree methods

"""

import unittest

from bst import *
from linked_list import *


class Test(unittest.TestCase):

    def test_to_list(self):
        bst = BST()
        self.assertEqual(bst.to_list(), [])
        bst.insert(3)
        self.assertEqual(bst.to_list(), [3])
        bst.insert(2)
        self.assertEqual(bst.to_list(), [2, 3])


if __name__ == "__main__":
    unittest.main()
