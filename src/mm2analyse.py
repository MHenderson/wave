# mm2analyse 21/01/09

from dbif import *

import sys
MM2file=sys.argv[1]
analysisFile=sys.argv[2]


dbin=getTables(MM2file)

components=dbin['components']
operations=dbin['operations']
parameters=dbin['parameters']
associations=dbin['associations']
messages=dbin['messages']

components1=proj(components,(0,1))
assoc=join(invert(components1),join(proj(associations,(1,2)),components1))
source=join(proj(messages,(1,2)),components1)
target=join(proj(messages,(1,3)),components1)

x=[(c1,m,c2) for (i,m,c1,c2) in messages \
if (c1,c2) not in proj(associations,(1,2)) and (c2,c1) not in proj(associations,(1,2))]
curious=join(invert(components1),join(x,components1))

u_c=[(c1,m,c2) for (i,m,c1,c2) in messages \
if (c1,c2) not in proj(associations,(1,2))]
uncoupled_messages=join(invert(components1),join(u_c,components1))

untested_components = diff(ran(components1),ran(target))

t_o = join(proj(operations,(1,0)),components1)
testable_operations = [(m+'()',c) for (m,c) in t_o if c not in untested_components]

untested_operations = diff(testable_operations,target)

dbout={'comp':proj(components1,(1,)), 'assoc':assoc,
       'source':source, 'target':target, #'curious': curious,
       'uncoupled_messages':curious,
       'untested_components':untested_components,
       'untested_operations':untested_operations}

putTables(analysisFile,dbout)





