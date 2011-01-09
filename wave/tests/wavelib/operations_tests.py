# Matthew Henderson, 27.12.2010 (Chandlers Ford)

import unittest

from wavelib.operations import dom
from wavelib.operations import dr
from wavelib.operations import invert
from wavelib.operations import join
from wavelib.operations import join2
from wavelib.operations import ran
from wavelib.operations import rr
from wavelib.operations import setify

d = [('a',)]
r = [('b',)]
s = [('a', 'b')]
t = [('b', 'c')]
w = [('a', 'b'), ('a', 'b')]

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

class TestInvert(unittest.TestCase):

    """
    Test invert operation.
    """

    def setUp(self):
        pass

    def test_invert(self):
        self.assertEqual(invert(s), [('b', 'a')])

class TestSetify(unittest.TestCase):

    """
    Test setify operation.
    """

    def setUp(self):
        pass

    def test_setify(self):
        self.assertEqual(setify(w), [('a', 'b')])

class TestDom(unittest.TestCase):

    """
    Test domain operator.
    """

    def setUp(self):
        pass

    def test_dom(self):
        self.assertEqual(dom(s), [('a',)])

class TestRan(unittest.TestCase):

    """
    Test range operator.
    """

    def setUp(self):
        pass

    def test_ran(self):
        self.assertEqual(ran(s), [('b',)])
        
class TestDR(unittest.TestCase):

    """
    Test domain restrict operator.
    """

    def setUp(self):
        pass

    def test_dr(self):
        self.assertEqual(dr(d, s), [('a','b')])
        
class TestRR(unittest.TestCase):

    """
    Test range restrict operator.
    """

    def setUp(self):
        pass

    def test_rr(self):
        self.assertEqual(rr(s, r), [('a','b')])
      
