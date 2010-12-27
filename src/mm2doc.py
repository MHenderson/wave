# mm2doc.py based onEAScript.py 17/12/08

from dbif import *

import sys
MM2file=sys.argv[1]
documentationFile=sys.argv[2]


dbin=getTables(MM2file)

components=dbin['components']
operations=dbin['operations']
parameters=dbin['parameters']
associations=dbin['associations']
messages=dbin['messages']

def html_table(tab):
    res="<table border=1>"
    for t in tab:
        res=res+"<tr>"
        for e in t:
            res=res+"<td>"+e+"</td>"
        res=res+"</tr>"
    res=res+"</table>"
    return res
def flat(T): return T[0][0]
def br(s):return s.replace("\n","<br/>")

doc=open(documentationFile,'w')
doc.write("""<html><head>
<style type="text/css">
<!--
h1 {color:black; font-family:sans-serif; font-size:120%}
h2 {color:black; font-family:sans-serif; font-size:80%;
margin-top:20px;
}
p {color:black; font-family:sans-serif; font-size:80%;
margin-top:20px;
}
.code {font-family:monospace; font-size:80%;
}
.doc_comp {font-family:sans-serif;
width:600px;
}
.doc_op {font-family:sans-serif; font-size:100%;
margin-left:20px;
width:580px;
}
-->
</style>
</head><body>""")
for c in dom(components):
    doc.write("<H1>Component - " + flat(dom(join([c],components))) + "</H1>")
    doc.write("<div class='doc_comp'>"+br(flat(ran(join([c],components))))+"</div>")
    for op in dom(join([c],operations)):
        doc.write("<div class='doc_op'>"+"<H2>Operation - " +flat([op])+"</H2>")
        p=join([op],join([c],parameters))
        doc.write("<div class='code'>"+flat([op])+"(")
        for i in range(1,len(p)-1):
            doc.write(flat(dom(join([(str(i),)],p)))+" : ")
            doc.write(flat(ran(join([(str(i),)],p)))+",")
        if len(p)>1:
            doc.write(flat(dom(join([(str(len(p)-1),)],p)))+" : ")
            doc.write(flat(ran(join([(str(len(p)-1),)],p))))
        doc.write("): ")
        doc.write(flat(ran(join([(str(0),)],p)))+"</div>")
        doc.write("<p>"+flat(join([op],join([c],operations)))+"</p>")
        doc.write("</div><br/>")
    doc.write("<hr/>")
        
                  
                  

doc.write("""</body></html>""")

doc.close()

