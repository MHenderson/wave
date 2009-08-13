import wx, wx.grid, dbif
            
class RelationTable(wx.grid.PyGridTableBase):
    
    def __init__(self, entries, name):
        wx.grid.PyGridTableBase.__init__(self)
        self.entries = entries
        self.name = name
	
    def GetNumberRows(self):
	return len(self.entries)

    def GetNumberCols(self):
        return 2

    def GetColLabelValue(self, col):
	return col

    def GetRowLabelValue(self, row):
	return row

    def IsEmptyCell(self, row, col):
	return False

    def GetValue(self, row, col):
	return self.entries[row][col]

    def SetValue(self, row, col, value):
	current_tuple = self.entries[row]
	self.entries[row] = current_tuple[:col] + (value,) + current_tuple[col+1:]

    def AppendRows(self, num_of_rows = 1):
	self.entries.append((0,0))

    def DeleteRows(self, num_of_rows = 1):
	self.entries.pop()

    def apply_dbif_operation(self, operation):
        self.entries = operation(self.entries)

class SimpleGrid(wx.grid.Grid):

    def __init__(self, parent, table):
        wx.grid.Grid.__init__(self, parent, -1, wx.Point(0, 0), wx.Size(600, 520))
	self.name = table.name
        self.SetTable(table) 

    def AppendRows(self, num_of_rows = 1):
	self.GetTable().AppendRows()
	self.SetTable(self.GetTable()) 

    def DeleteRows(self, pos = 0, numRows = 1, updateLabels = False):
	self.GetTable().DeleteRows()
	self.SetTable(self.GetTable()) 

    def apply_dbif_operation(self, operation):
        self.GetTable().apply_dbif_operation(operation)
        self.SetTable(self.GetTable())

def apply_dbif_operation(operation, grid1, grid2):
    table1 = grid1.GetTable()
    table2 = grid2.GetTable()
    entries1 = table1.entries
    entries2 = table2.entries
    result_entries = operation(entries1, entries2)
    result_table = RelationTable(result_entries, '')
    return result_table

