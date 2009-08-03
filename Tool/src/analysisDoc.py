# analysisDoc 21/01/09

from dbif import *

import sys

analysisFile=sys.argv[1]
analysisDocFile=sys.argv[2]

dbin=getTables(analysisFile)

comp=dbin['comp']
assoc=dbin['assoc']
source=dbin['source']
target=dbin['target']
uncoupled_messages=dbin['uncoupled_messages']
untested_components=dbin['untested_components']
untested_operations=dbin['untested_operations']

def html_table(tab):
    if tab==[]: return "<p>THIS TABLE IS EMPTY."
    res="<p><table border=1 cellspacing=0>"
    for t in tab:
        res=res+"<tr>"
        for e in t:
            res=res+"<td>"+e+"</td>"
        res=res+"</tr>"
    res=res+"</table>"
    return res
def flat(T): return T[0][0]
def br(s):return s.replace("\n","<br/>")

doc=open(analysisDocFile,'w')
doc.write("""<html><head>
<style type="text/css">
<!--
td {color:black; font-family:sans-serif; font-size:80%}
h1 {color:black; font-family:sans-serif; font-size:140%}
h2 {color:black; font-family:sans-serif; font-size:120%}
h3 {color:black; font-family:sans-serif; font-size:80%;
margin-top:20px;
}
p {color:black; font-family:sans-serif; font-size:100%;
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
</head><body>
<h1>Report on the analysis of an MM2 Model</h1>
<p>Model - MOSAv3G
<p>MM - version 2 (temp fix)
<p>Date - January 9, 2009""")

doc.write("""<hr/>
<h2>Untested Components</h2>

<p>In the following table you will find a list of Components that exist
in your model but are not used in any Sequence Diagram.
""")

doc.write(html_table(untested_components))

doc.write("""<hr/>
<h2>Untested Messages</h2>

<p>In the following table you will find messages 
in your model that are not used in any Sequence Diagram. This table excludes messages
to Components listed as "Untested Components". 

<p>The columns are respectively - The Message and The Sink.""")

doc.write(html_table(untested_operations))

doc.write("""<hr/>
<h2>Uncoupled Messages</h2>

<p>In the following table you will find messages that exist
in your model but are between
Components that are not properly associated.

<p>The columns are respectively - The Source, The Message and The Sink.
""")

doc.write(html_table(uncoupled_messages))
              
doc.write("""<hr/>
<h2>Message Sources</h2>

<p>In the following table you will find Components related to Messages of which they are
the source.

<p>The columns are respectively - The Source and The Message.""")

doc.write(html_table(invert(source)))
              

doc.write("""<hr/>
<h2>Message Targets</h2>

<p>In the following table you will find Components related to Messages of which they are
the target.

<p>The columns are respectively - The Message and The Target.
""")

doc.write(html_table(target))
              
doc.write("""<hr/>
<h2>Associations</h2>

<p>In the following table you will find listed the
Associations between Components.
""")


doc.write(html_table(assoc))
              


doc.write("""</body></html>""")

doc.close()

