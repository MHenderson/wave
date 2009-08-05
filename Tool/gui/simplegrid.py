import wx, wx.grid
            
class RelationTable(wx.grid.PyGridTableBase):

	colLabels = ["Source", "Target"]
	rowLabels = ["0", "1"]

	def __init__(self, entries):
		wx.grid.PyGridTableBase.__init__(self)
		self.entries = entries

	def GetNumberRows(self):
		return len(self.entries)

	def GetNumberCols(self):
		return 2

	def GetColLabelValue(self, col):
		return self.colLabels[col]

	def GetRowLabelValue(self, row):
		return self.rowLabels[row]

	def IsEmptyCell(self, row, col):
		return False

	def GetValue(self, row, col):
		return self.entries[row][col]

	def SetValue(self, row, col, value):
		current_tuple = self.entries[row]
		new_tuple = current_tuple[:col] + (value,) + current_tuple[col+1:]
		self.entries[row] = new_tuple

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent, data):
        wx.grid.Grid.__init__(self, parent, -1, wx.Point(0, 0), wx.Size(600, 600))
        tableBase = RelationTable(data)
        self.SetTable(tableBase) 

