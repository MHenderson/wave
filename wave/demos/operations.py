import Wave, dbif
from Wave import metamodel

join = Wave.metamodel.Function(dbif.join, fix = 'in', symbol = '.')
diff = Wave.metamodel.Function(dbif.diff, fix = 'in', symbol = '-')
invert = Wave.metamodel.Function(dbif.invert, fix = 'pre', symbol = '~')
close =  Wave.metamodel.Function(dbif.close, fix = 'pre', symbol = '^')
mm = Wave.metamodel.Metamodel()
mm.add_function(join, 'join', 'join')
mm.add_function(diff, 'diff', 'diff')
mm.add_function(invert, 'invert', 'invert')
mm.add_function(close, 'close', 'close')

