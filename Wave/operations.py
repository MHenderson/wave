def join(r1,r2): 
    """
    This is dot join from Alloy. Both arguments are dbif-tables, as is the 
    result. Tuples are joined when the last element of a tuple from r1 is equal
    to the first element of a tuple from r2. The common element is dropped.
    """
    return [t1[0:-1] + t2[1:] for t1 in r1 for t2 in r2 if t1[-1] == t2[0]]

def join2(r1,r2):
    """
    This is circle-dot join from Alloy. Both arguments are dbif-tables, as 
    is the result. Tuples are joined when the last element of a tuple from r1 
    is equal to the first element of a tuple from r2. The common element is 
    retained.
    """
    return [t1[0:-1] + t2[0:] for t1 in r1 for t2 in r2 if t1[-1] == t2[0]]
    
def invert(r): 
    """
    This is twiddle from Alloy. All tuples in the dbif-table r are reversed.
    """
    return [t[-1::-1] for t in  r]

def setify(t):
    """
    Remove duplicate tuples from dbif-table t.
    """
    return list(set(t))
    
def dom(r): 
    """
    Domain of a relation. Argument is a dbif-table (i.e. a multi-relation).
    """
    return setify([(t[0],) for t in r])

def ran(r):
    """
    Range of a relation. Argument is a dbif-table (i.e. a multi-relation).
    """
    return setify([(t[-1],) for t in r])

def dr(s,r):
    """
    Alloy operator <: - Domain-restrict a relation. First argument is a 'set' 
    (a dbif-table with tuples of length 1. Second argument is a dbif-table. 
    Result is a dbif-table, same as r but with first column entries restriced 
    to elements in s.
    """
    return setify([t for t in r if (t[0],) in s])

def rr(r,s):
    """
    Alloy operator :> - Range-restrict a relation. First argument is a 
    dbif-table. Second argument is a 'set' (a dbif-table with tuples of length
    1. Result is a dbif-table, same as r but with last column entries restriced
    to elements in s.
    """
    return setify([t for t in r if (t[-1],) in s])

def close(r):
    """
    Transitive closure of a relation.
    """
    res=r
    cand=join(r,r)
    while not inc(cand,res):
        res=res+cand
        cand=join(r,cand)
    return res

def inc(r1,r2):
    """
    Arguments are dbif-tables. Result is Boolean. True if r1 is a subset of r2.
    Implements Alloy operator 'in' (which is both subset and membership-test, 
    see book).
    """
    return all((t in r2) for t in r1)

def iden(r):
    """
    Implements Alloy constant 'iden' as best as possible. returns Identity 
    relation whose basis is all the elements used by the dbif-table r.
    """
    return [(a,a) for a in setify([a for t in r for a in t])]

def prn(a):
    """
    Print a relation.
    """
    for line in a:
        print(string.join(line,'\t').strip())
    print("----")

def union(t1, t2):
    """
    Union of relations.
    """
    return list(set(t1).union(set(t2)))

def inter(t1, t2):
    """
    Intersection of relations.
    """
    return list(set(t1).intersection(set(t2)))

def diff(t1, t2):
    """
    Difference of relations.
    """
    return list(set(t1).difference(set(t2)))
            
def prod(t1, t2):
    """
    Product of relations.
    """
    return [a + b for a in t1 for b in t2]

def proj(t1, p):
    """
    Project columns of a relation (a dbif table) t1. The second argument is
    a tuple of integers which are column numbers used to permute the entries in
    t1.
    """
    return list(set([tuple(a[i] for i in p) for a in t1]))

def sel(t1, p):
    """
    Select rows of a relation (a dbif table) t1. The second argument is a 
    Python expression with free variable 'r' which computes a Boolean value 
    for each row in t1. Rows selected atre those for which p returns true.
    """
    return list(set([a for a in t1 if eval(p,{'r':a})]))

def collect(r):
    """
    XXX collect documentation XXX
    """
    return [(t[0],frozenset(join([(t[0],)],r))) for t in dom(r)]

def subjoin(r1,r2):
    """
    XXX subjoin documentation XXX
    """
    return [t1[0:-1]+t2[1:] for t1 in r1 for t2 in r2 if inc(t1[-1],t2[0])]

