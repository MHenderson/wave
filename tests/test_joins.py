import wharve as wv

def test_join():
    assert wv.join([('a', 'b')], [('b', 'c')]) == [('a', 'c')]

def test_join2():
    assert wv.join([('a', 'b')], [('b', 'c')]) == [('a', 'b', 'c')]

