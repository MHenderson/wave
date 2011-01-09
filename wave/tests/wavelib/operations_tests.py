# Matthew Henderson, 27.12.2010 (Chandlers Ford)

import unittest

from wavelib.operations import close
from wavelib.operations import collect
from wavelib.operations import diff
from wavelib.operations import dom
from wavelib.operations import dr
from wavelib.operations import iden
from wavelib.operations import inc
from wavelib.operations import inter
from wavelib.operations import invert
from wavelib.operations import join
from wavelib.operations import join2
from wavelib.operations import prod
from wavelib.operations import proj
from wavelib.operations import ran
from wavelib.operations import rr
from wavelib.operations import sel
from wavelib.operations import setify
from wavelib.operations import subjoin
from wavelib.operations import union

d = [('a',)]
r = [('b',)]
s = [('a', 'b')]
t = [('b', 'c')]
w = [('a', 'b'), ('a', 'b')]
q = [('a', 'b'), ('b', 'c')]

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
      
class TestClose(unittest.TestCase):

    """
    Test transitive closure operator.
    """

    def setUp(self):
        pass

    def test_close(self):
        self.assertEqual(close(q), [('a', 'b'), ('b', 'c'), ('a','c')])

class TestInc(unittest.TestCase):

    """
    Test subset/membership.
    """

    def setUp(self):
        pass

    def test_inc(self):
        self.assertFalse(inc(s,t))
    
class TestIden(unittest.TestCase):

    """
    Test identity relation.
    """

    def setUp(self):
        pass

    def test_iden(self):
        self.assertEqual(iden(s), [('a','a'),('b','b')])

class TestUnion(unittest.TestCase):

    """
    Test union relation.
    """

    def setUp(self):
        pass

    def test_union(self):
        self.assertEqual(union(s, t), [('a','b'),('b','c')])
        
class TestInter(unittest.TestCase):

    """
    Test intersection relation.
    """

    def setUp(self):
        pass

    def test_inter(self):
        self.assertEqual(inter(s, t), [])
           
class TestDiff(unittest.TestCase):

    """
    Test relational difference.
    """

    def setUp(self):
        pass

    def test_diff(self):
        self.assertEqual(diff(s, t), [('a','b')])

class TestProd(unittest.TestCase):

    """
    Test relational product.
    """

    def setUp(self):
        pass

    def test_prod(self):
        self.assertEqual(prod(s, t), [('a','b','b','c')])

class TestProj(unittest.TestCase):

    """
    Test projection.
    """

    def setUp(self):
        pass

    def test_proj(self):
        self.assertEqual(proj(s, (1,0)), [('b','a')])

class TestSel(unittest.TestCase):

    """
    Test selection.
    """

    def setUp(self):
        pass

    def test_sel(self):
        self.assertEqual(sel(s, "True"), [('a','b')])

class TestCollect(unittest.TestCase):

    """
    Test collect.
    """

    def setUp(self):
        pass

    def test_collect(self):
        self.assertEqual(collect(s), [('a', frozenset([('b',)]))])

class TestSubjoin(unittest.TestCase):

    """
    Test subjoin.
    """

    def setUp(self):
        pass

    def test_subjoin(self):
        self.assertEqual(subjoin(s,t), [('a', 'c')])
