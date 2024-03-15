import MySQLdb
import string

HOST = "localhost"
DATABASE = "test"
DEBUGGING = False

"""In the following, it is important to distinguish between a mySQL table and a dbif-table. A mySQL table is a table in the mySQL database. A dbif-table is a list of tuples of strings (there should be no duplicate tuples). Alloy refers to a multi-relation, i.e. a set of n-tuples where n can be any integer, not just 2. A dbif-table is the Python structure used for multi-relation. Some functions move tables between mySQL and Python, others operate only on dbif-tables"""

def use(db):
    """Use a database."""
    global DATABASE
    DATABASE = db

def do(command):
    """Do a mySQL command. Return a dbif-table."""
    if DEBUGGING:
        print("do - " + command)
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

def recompute():
    """Used only by a crafty mySQL 'trick'. Database must have a table called 'vtable' whose enties are table names and Python expressions that construct dbif-tables. Calling recompute creates new 'real' tables in the database corresponding to the entries in vtable. Will overwrite any existing tables. I need this for the CGI script only."""
    try:
        vtables = get("vtable")
    except:
        return
    for (table,) in do("show tables"):
        exec(table + ' = get("' + table + '")')
    for (table, expr) in vtables:
        exec(table + ' = ' + expr)
        put(table, eval(table))

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

