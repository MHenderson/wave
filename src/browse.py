#!/usr/bin/env python
# browse.py 30/7/08

from dbif import *
import cgi

print 'Content-type: text/html'
print
print '<html><body>'
##### COLLECT PARAMETERS
form=cgi.FieldStorage()
tup=() # a tuple to be inserted 
if form.has_key("button") and form["button"].value=="update":
    for i in range(0,6):
        if form.has_key("col"+str(i)):
            tup=tup+(form["col"+str(i)].value,)
row2go=-1 # a row to be deleted
if form.has_key("button") and form["button"].value=="delete":
    if form.has_key("row2go"):
        try:
            row2go=int(form["row2go"].value)-1
        except:
            row2go=-1
newtable="" # table to create
if form.has_key("button") and form["button"].value=="new_table":
    if form.has_key("newtable"):
        try:
            newtable=form["newtable"].value
        except:
            newtable=""
table2go="" # table to delete
if form.has_key("button") and form["button"].value=="delete_table":
    if form.has_key("newtable"):
        try:
            table2go=form["newtable"].value
        except:
            table2go=""
table2copy="" # table to copy
if form.has_key("button") and form["button"].value=="copy_table":
    if form.has_key("newtable"):
        try:
            table2copy=form["newtable"].value
        except:
            table2copy=""
new_db="" # new database
if form.has_key("button") and form["button"].value=="new_db":
    if form.has_key("newtable"):
        try:
            new_db=form["newtable"].value
        except:
            new_db=""
db2go="" # new database
if form.has_key("button") and form["button"].value=="delete_db":
    if form.has_key("newtable"):
        try:
            db2go=form["newtable"].value
        except:
            db2go=""
db2copy="" # new database
if form.has_key("button") and form["button"].value=="copy_db":
    if form.has_key("newtable"):
        try:
            db2copy=form["newtable"].value
        except:
            db2copy=""
dbname="" # the database to use
if form.has_key("dbname"):
    dbname=form["dbname"].value
    use(dbname)
name=""; n=0 # rthe table to use
if form.has_key("name"):
    name=form["name"].value
    try:
        table=get(name)
        n=len(table[0])
    except:
        table=[]
        n=0
#### PERFORM ACTIONS
try:
    table=get(name)
    if table!=[] and len(tup)==len(table[0]): table=table+[tup]
    elif table==[] and len(tup)>0:table=table+[tup]        
    if row2go>=0 and row2go<len(table):
        print 'deleted',table[row2go]
        table=diff(table,[table[row2go]])
    table.sort()
    put(name,table)
except: pass
if newtable!="":put(newtable,[])
if table2go!="":do('drop table '+table2go)
if table2copy!="":put(table2copy,get(name))
if new_db!="":do('create database '+new_db)
if db2go!="":do('drop database '+db2go)
if db2copy!="":copydatabase(db2copy)
recompute()

###### FORM STARTS HERE
print """
<form method="POST" action="http://localhost/scripts/browse.py">
database: <select name="dbname" size=1>
"""
databases=do("show databases")
for database in databases:
    if database[0]==dbname: print '<option selected>',database[0],'</option>'
    elif database[0]=='information_schema': pass
    else: print '<option>',database[0],'</option>'
print """
</select>
table: <select name="name" size=1>
"""
tables=do("show tables")
for table in tables:
    if table[0]==name: print '<option selected>',table[0],'</option>'
    else: print '<option>',table[0],'</option>'
print """
</select>
<input type="submit" name="button" value="query">
<input type="submit" name="button" value="update">
<table border=1 width=100%><tr>
"""
if n==0: n=6
for i in range(0,n):
    print """<td><input size=50 name="col"""+str(i)+""""></td>"""
print """
</tr></table>
<input type="submit" name="button" value="delete">
<input name="row2go">
<input name="newtable">
<input type="submit" name="button" value="new_table">
<input type="submit" name="button" value="copy_table">
<input type="submit" name="button" value="delete_table">
<input type="submit" name="button" value="new_db">
<input type="submit" name="button" value="copy_db">
<input type="submit" name="button" value="delete_db">
</form>
"""

# TABLE BEGINS HERE
try:
    table=get(name)
    n=len(table[0]); i=0;
    print '<table border=1 width=100%>'
    for tup in table:
        i=i+1
        print '<tr>', '<td bordercolor="white" width=100 align="right">',i,'</td>'
        for ent in tup:
            print '<td>',ent,'</td>'
        print '</tr>'
    print '</table>'
except:
    pass
print '</body></html>'



