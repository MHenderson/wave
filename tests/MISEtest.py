from dbif import *

source=[('A1','C1'),('A2','C2'),('A3','C3')]
target=[('A1','C2'),('A2','C3'),('A3','C1')]
sender=[('M1','C1'),('M2','C2'),('M3','C2')]
receiver=[('M1','C2'),('M2','C3'),('M3','C1')]
method=[('M1','op2'),('M2','op3'),('M3','op1')]
operations=[('C1','op1'),('C2','op2'),('C3','op3'),('C3','op99')]
components=[('C1',),('C2',),('C3',)]
print 'messages to components that are not associated'
print diff(join(invert(sender),receiver),join(invert(source),target))
print 'messages that are not tested'
print diff(join(invert(source),target),join(invert(sender),receiver))
print 'methods that are not allowed'
print diff(method,join(receiver,operations))
print 'methods that are not tested'
print diff(operations,join(invert(receiver),method))
print 'messages as 3 tuples'
print join2(invert(sender),receiver)
print 'components that are not tested'
print diff(components, ran(receiver))



def rest(r1,p,r2):
    return [t for t in r1 if tuple(t[i] for i in p) in r2]

print rest(join2(invert(sender),receiver),
           (0,2),
           diff(join(invert(sender),receiver),join(invert(source),target)))

           
