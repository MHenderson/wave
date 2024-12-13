def diff(t1, t2):
    """
    Difference of relations.

    :param t1: A dbif-table.
    :param t2: A dbif-table.
    :return A dbif-table representing the difference of t1 and t2.
    """
    return list(set(t1).difference(set(t2)))

def invert(r): 
    """
    Twiddle from Alloy.
    
    All tuples in the dbif-table r are reversed.

    :param r: A dbif-table.
    :return A dbif-table representing the twiddle of r.
    """
    return [t[-1::-1] for t in  r]

def join(r1, r2): 
    """
    This is dot join from Alloy. Both arguments are dbif-tables, as is the 
    result. Tuples are joined when the last element of a tuple from r1 is equal
    to the first element of a tuple from r2. The common element is dropped.

    :param r1: A dbif-table.
    :param r2: A dbif-table.
    :return A dbif-table representing the dot join of r1 and r2.
    """
    return [t1[0:-1] + t2[1:] for t1 in r1 for t2 in r2 if t1[-1] == t2[0]]

def join2(r1, r2):
    """
    This is circle-dot join from Alloy. Both arguments are dbif-tables, as 
    is the result. Tuples are joined when the last element of a tuple from r1 
    is equal to the first element of a tuple from r2. The common element is 
    retained.

    :param r1: A dbif-table.
    :param r2: A dbif-table.
    :return A dbif-table representing the circle-dot join of r1 and r2.
    """
    return [t1[0:-1] + t2[0:] for t1 in r1 for t2 in r2 if t1[-1] == t2[0]]
 
