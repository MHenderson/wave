# Peter Henderson, 25.09.08 (Southampton)

import MySQLdb
import string

HOST = "localhost"
DATABASE = "test"
DEBUGGING = False

"""In the following, it is important to distinguish between a mySQL table
and a dbif-table. A mySQL table is a table in the mySQL database. A dbif-table
is a list of tuples of strings (there should be no duplicate tuples). Alloy
refers to a multi-relation, i.e. a set of n-tuples where n can be any
integer, not just 2. A dbif-table is the Python structure used for multi-relation.
Some functions move tables between mySQL and Python, others operate only on
dbif-tables"""

def use(db):
    """Use a database."""
    global DATABASE
    DATABASE = db

def do(command):
    """Do a mySQL command. Return a dbif-table."""
    if DEBUGGING:
        print "do - " + command
    connection = MySQLdb.connect(host = HOST, db = DATABASE)
    cursor = connection.cursor()
    resultSet = []
    cursor.execute(command)
    while (1):
        row = cursor.fetchone()
        if row == None:
            break
        resultSet = resultSet + [row]
    cursor.close()
    connection.commit()
    connection.close()
    return resultSet

def get(table):
    """Get a table from the database. Return a dbif-table."""
    return do("select * from " + table)
     
def put(table, rows):
    """Put the rows (a dbif-table) into the database as the mySQL table."""
    if rows == []:
        return
    rank = len(rows[0])
    try:
        do("drop table if exists " + table)
    except:
        pass
    fields = ""
    for i in range(0, rank):
        fields = fields + "col" + str(i) + " text,"
    do("create table " + table + " (" + fields[0:-1] + ")")
    fields=""
    for i in range(0,rank):
        fields = fields + "col" + str(i) + "(30),"
    do("alter table " + table + " add primary key(" + fields[0:-1] + ")")
    for row in rows:
        if len(row) == 1:
            do("insert into " + table + " values ('" + row[0] + "')")
        else:
            do("insert into " + table + " values " + str(row))

def save(table):
    """Copy a mySQL table T by creating a new table called saved_T"""
    put('saved_' + table, get(table))

def restore(table):
    """Restore a saved mySQL table."""
    put(table, get('saved_' + table))

def join(r1,r2): 
    """This is dot join from Alloy. Both arguments are dbif-tables, as is the
result. Tuples are joined when the last element of a tuple from r1 is equal to
the first element of a tuple from r2. The common element is dropped."""
    return [t1[0:-1] + t2[1:] for t1 in r1 for t2 in r2 if t1[-1] == t2[0]]

def join2(r1,r2):
    """This is circle-dot join from Alloy. Both arguments are dbif-tables, as is the
result. Tuples are joined when the last element of a tuple from r1 is equal to
the first element of a tuple from r2. The common element is retained."""
    return [t1[0:-1] + t2[0:] for t1 in r1 for t2 in r2 if t1[-1] == t2[0]]
    
def invert(r): 
    """This is twiddle from Alloy. All tuples in the dbif-table r
are reversed"""
    return [t[-1::-1] for t in  r]

def setify(t):
    """Remove duplicate tuples from dbif-table t."""
    return list(set(t))
    
def dom(r): 
    """Domain of a relation. Argument is a dbif-table (i.e. a multi-relation)."""
    return setify([(t[0],) for t in r])

def ran(r):
    """Range of a relation. Argument is a dbif-table (i.e. a multi-relation)."""
    return setify([(t[-1],) for t in r])

def dr(s,r):
    """Alloy operator <: - Domain-restrict a relation. First argument is a 'set' (a dbif-table with
tuples of length 1. Second argument is a dbif-table. Result is a dbif-table,
same as r but with first column entries restriced to elements in s."""
    return setify([t for t in r if (t[0],) in s])

def rr(r,s):
    """Alloy operator :> - Range-restrict a relation. First argument is a
dbif-table. Second argument is a 'set' (a dbif-table with
tuples of length 1. Result is a dbif-table,
same as r but with last column entries restriced to elements in s."""
    return setify([t for t in r if (t[-1],) in s])

def close(r):
    """Transitive closure of a relation."""
    res=r
    cand=join(r,r)
    while not inc(cand,res):
        res=res+cand
        cand=join(r,cand)
    return res

def inc(r1,r2):
    """Arguments are dbif-tables. Result is Boolean. True if r1 is a
subset of r2. Implements Alloy operator 'in' (which is both subset and membership
-test, see book)"""
    return all((t in r2) for t in r1)

def iden(r):
    """Implements Alloy constant 'iden' as best as possible. returns Identity
relation whose basis is all the elements used by the dbif-table r."""
    return [(a,a) for a in setify([a for t in r for a in t])]

def prn(a):
    """Print a relation."""
    for line in a:
        print string.join(line,'\t').strip()
    print "----"

def union(t1, t2):
    """Union of relations."""
    return list(set(t1).union(set(t2)))

def inter(t1, t2):
    """Intersection of relations."""
    return list(set(t1).intersection(set(t2)))

def diff(t1, t2):
    """Difference of relations."""
    return list(set(t1).difference(set(t2)))
            
def prod(t1, t2):
    """Product of relations."""
    return [a + b for a in t1 for b in t2]

def proj(t1, p):
    """Project columns of a relation (a dbif table) t1. The second argument is a
tuple of integers which are column numbers used to permute the entries
in t1."""
    return list(set([tuple(a[i] for i in p) for a in t1]))

def sel(t1, p):
    """Select rows of a relation (a dbif table) t1. The second argument is a
Python expression with free variable 'r' which computes a Boolean value for each
row in t1. Rows selected atre those for which p returns true."""
    return list(set([a for a in t1 if eval(p,{'r':a})]))

def recompute():
    """Used only by a crafty mySQL 'trick'. Database must have a table
called 'vtable' whose enties are table names and Python expressions that
construct dbif-tables. Calling recompute creates new 'real' tables in
the database corresponding to the entries in vtable. Will overwrite any
existing tables. I need this for the CGI script only."""
    try:
        vtables = get("vtable")
    except:
        return
    for (table,) in do("show tables"):
        exec table + ' = get("' + table + '")'
    for (table, expr) in vtables:
        exec table + ' = ' + expr
        put(table, eval(table))

def collect(r):
    return [(t[0],frozenset(join([(t[0],)],r))) for t in dom(r)]

def subjoin(r1,r2):
    return [t1[0:-1]+t2[1:] for t1 in r1 for t2 in r2 if inc(t1[-1],t2[0])]

#  dbifXML (copied, modified to avoid eval/exec)

import xml.dom.minidom
import xml.sax.saxutils

#putTables - take list of tables and create an XML file
#getTables - read XML file that contains a database and construct tables

stylesheet=""
def setStylesheet(ss):
     global stylesheet
     stylesheet=ss

def putTables(fn,Tdic):
    doc=open(fn,'w');
    doc.write("""<?xml version="1.0" encoding="utf-8"?>""")
    if stylesheet!="":
         doc.write('<?xml-stylesheet type="text/xsl" href="'+stylesheet+'"?>')
    doc.write("<dbifDatabase>")
    for Tname,T in Tdic.items():
        doc.write('<dbifTable name="'+Tname+'">')
        for r in T:
            doc.write("<dbifRow>")
            for e in r:
                doc.write("<dbifEl>"+xml.sax.saxutils.escape(e)+"</dbifEl>")
            doc.write("</dbifRow>")
        doc.write("</dbifTable>")
    doc.write("</dbifDatabase>"); doc.close()

def getTables(fn):
    document=open(fn); Tdic={}
    doc = xml.dom.minidom.parse(document)
    elem=doc.childNodes[-1]
    Tables=elem.getElementsByTagName("dbifTable"); tables=[]
    for T in Tables:
        Tname=T.getAttribute("name"); tables=tables+[Tname]
        Rows=T.getElementsByTagName("dbifRow"); table=[]
        for r in Rows:
            els=r.getElementsByTagName("dbifEl"); row=tuple()
            for el in els:
                 if el.hasChildNodes():
                      row=row+(xml.sax.saxutils.unescape(el.firstChild.nodeValue),)
                 else: row=row+(" ",)
            table=table+[row]
        Tdic[safestr(Tname)]=deUnicode(table)
    return Tdic
    
def safestr(u):
    try: return str(u)
    except: return "?"
def deUnicode(T):
    return [tuple(safestr(e) for e in t) for t in T]
