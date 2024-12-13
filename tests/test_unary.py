import wharve as wv

def test_invert():
  assert wv.invert([('a', 'b')]) == [('b', 'a')]
  assert wv.invert([('a', 'b'), ('c', 'd')]) == [('b', 'a'), ('d', 'c')]
