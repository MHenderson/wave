import wharve as wv

def test_diff():
    assert wv.diff([('a', 'b'), ('b', 'c')], [('a', 'b')]) == [('b', 'c')]

def test_join():
    assert wv.join([('a', 'b')], [('b', 'c')]) == [('a', 'c')]

def test_join2():
    assert wv.join2([('a', 'b')], [('b', 'c')]) == [('a', 'b', 'c')]

