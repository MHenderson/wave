# Matthew Henderson, 27.12.2010 (Chandlers Ford)

import unittest

from wavelib.operations import join

class TestJoin(unittest.TestCase):
    """Test join operation."""

    def setUp(self):
        self.s = [('a', 'b')]
        self.t = [('b', 'c')]
        self.st = [('a', 'c')]

    def test_join(self):
        self.assertEqual(join(self.s,self.t), self.st)

