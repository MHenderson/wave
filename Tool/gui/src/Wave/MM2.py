import dbif
from dbif import join, diff, dr, dom

import Wave
from Wave import metamodel

def DR(contains, requires, supplies):
    return diff(diff(join(contains, requires), join(contains, supplies)), requires)

def DS(contains, supplies):
    return diff(dr(dom(contains), supplies), join(contains, supplies))

DR = Wave.metamodel.Function(DR, name = 'dr')
DS = Wave.metamodel.Function(DS, name = 'ds')
mm = Wave.metamodel.Metamodel()
mm.add_function(DR, 'dr', 'dangling_requires')
mm.add_function(DS, 'ds', 'dangling_supplies')

