# Matthew Henderson, 27.12.2010 (Chandlers Ford)

import unittest

from wavelib.operations import join
from wavelib.operations import join2

s = [('a', 'b')]
t = [('b', 'c')]

class TestJoin(unittest.TestCase):

    """
    Test join operation.
    """

    def setUp(self):
        pass

    def test_join(self):
        self.assertEqual(join(s, t), [('a', 'c')])

class TestJoin2(unittest.TestCase):

    """
    Test join2 operation.
    """

    def setUp(self):
        pass

    def test_join2(self):
        self.assertEqual(join2(s, t), [('a', 'b', 'c')])

