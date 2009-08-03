# xmi2mm2.py 21/01/09, for use with MMX

import xml.dom.minidom
import sys
XMIfile=sys.argv[1]
MM2file=sys.argv[2]

print "opening ", XMIfile
document = open(XMIfile)
doc = xml.dom.minidom.parse(document)
elem=doc.childNodes[1]

from dbif import *

def getMessages():
    M=elem.getElementsByTagName("UML:Message"); messages=[]
    for m in M:
        messages=messages+[(m.getAttribute("xmi.id"),
                           m.getAttribute("name"),
                           m.getAttribute("sender"),
                           m.getAttribute("receiver"))]
    return messages

def getComponents():
    C=elem.getElementsByTagName("UML:Component"); components=[]
    for c in C:
        components=components+[(c.getAttribute("xmi.id"),
                           c.getAttribute("name"),getDocumentation(c))]
    return components

def getOperations():
    C=elem.getElementsByTagName("UML:Component"); operations=[]
    for c in C:
        Ops=c.getElementsByTagName("UML:Operation")
        for op in Ops:
           operations=operations+[(c.getAttribute("xmi.id"),
                           op.getAttribute("name"),getDocumentation(op))]
    return operations

def getParameters():
    C=elem.getElementsByTagName("UML:Component"); parameters=[]
    for c in C:
        Ops=c.getElementsByTagName("UML:Operation")
        for op in Ops:
            P=op.getElementsByTagName("UML:Parameter")
            i=0
            for p in P:
                parameters=parameters+[(c.getAttribute("xmi.id"),
                           op.getAttribute("name"),str(i),  
                           p.getAttribute("name"),
                           getParameterType(p))]
                i=i+1
    return parameters
def getParameterType(p):
    tvs=p.getElementsByTagName("UML:TaggedValue")
    for tv in tvs:
        if tv.getAttribute("tag")=="type":return tv.getAttribute("value")
    return "noTypeGiven"

def getAssociations():
    A=elem.getElementsByTagName("UML:Association"); associations=[]
    for a in A:
        ends=a.getElementsByTagName("UML:AssociationEnd")
        associations=associations+[(a.getAttribute("xmi.id"),
                                    ends[0].getAttribute("type"),
                                    ends[1].getAttribute("type"))]
    return associations

def getDocumentation(elem):
    tvs=getTaggedValues(elem)
    for tv in tvs:
        if tv.getAttribute("tag")=="documentation":return tv.getAttribute("value")
    return "No documentation available"
def getTaggedValues(elem):
    ch=elem.childNodes
    for c in ch:
        if c.nodeType==1 and c.tagName=="UML:ModelElement.taggedValue":
            return c.getElementsByTagName("UML:TaggedValue")
    return []

def safestr(u):
    try: return str(u)
    except: return "?"
def deUnicode(T):
    return [tuple(safestr(e) for e in t) for t in T]

components=deUnicode(getComponents())
operations=deUnicode(getOperations())
parameters=deUnicode(getParameters())
associations=deUnicode(getAssociations())
messages=deUnicode(getMessages())

dic={'components':components,'operations':operations,
     'parameters':parameters, 'associations':associations,
     'messages':messages}

print "opening ", MM2file
putTables(MM2file,dic)
close(MM2file)
