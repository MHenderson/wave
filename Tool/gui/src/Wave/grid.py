import wx, wx.grid
           
class Relation():

    """Basic representation of relations."""

    def __init__(self, table = []):
        self.table = table

    def __delitem__(self, index):
        del self.table[index]

class WaveGridTable(wx.grid.PyGridTableBase, Relation):

    """Custom WAVE GridTable class.
    
       Adapts a Wave Table for use as a grid table.
    """
    
    def __init__(self, relation):
        wx.grid.PyGridTableBase.__init__(self)
        self.relation = relation

    def GetNumberRows(self):
        return len(self.relation.table)

    def GetNumberCols(self):
        return 2

    def GetColLabelValue(self, col):
        return col

    def GetRowLabelValue(self, row):
        return row

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.relation.table[row][col]

    def SetValue(self, row, col, value):
        current_tuple = self.relation.table[row]
        self.relation.table[row] = current_tuple[:col] + (value,) + current_tuple[col+1:]

    def AppendRows(self, num_of_rows = 1):
        self.relation.table.append((0,0))

    def DeleteRows(self, pos = 0, numRows = 1, updateLabels = False):
        del self.relation[pos]

class WaveGrid(wx.grid.Grid):

    def __init__(self, parent, grid_table):
        wx.grid.Grid.__init__(self, parent, -1, wx.Point(0, 0), wx.Size(600, 520))
        self.grid_table = grid_table
        self.SetTable(self.grid_table) 

    def AppendRows(self, num_of_rows = 1):
        self.GetTable().AppendRows()
        self.SetTable(self.GetTable()) 

    def DeleteRows(self, pos = 0, numRows = 1, updateLabels = False):
        self.GetTable().DeleteRows(pos, numRows, updateLabels)
        self.SetTable(self.GetTable()) 


## apply_dbif_operation
#
#  Applies a dbif operation to a collection of WaveGrid objects.
#
#  \todo Refactor into two components - one which handles Relations and
#        another which, for convenience, handles grids.

def apply_dbif_operation(operation, *grids):
    grid_tables = [grid.GetTable() for grid in grids]
    relations = [grid_table.relation for grid_table in grid_tables]
    relation_tables = [relation.table for relation in relations]
    result_table = operation(*relation_tables)
    return result_table

def apply_to_relations(operation, *relations):
    relation_tables = [relation.table for relation in relations]
    result_table = operation(*relation_tables)
    result_relation = Relation(result_table)
    return result_relation

def apply_to_grid_tables(operation, *grid_tables):
    relations = [grid_table.relation for grid_table in grid_tables]
    result_relation = apply_to_relations(operation, *relations)
    result_grid_table = WaveGridTable(result_relation)
    return result_grid_table

