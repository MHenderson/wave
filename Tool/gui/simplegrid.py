import wx, wx.grid
            
class RelationTableElement:

	def __init__(self, source, target):
		self.source = source
		self.target = target

class RelationTable(wx.grid.PyGridTableBase):

	colLabels = ("Source", "Target")
	colAttrs = ("source", "target")

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
		return "X"

	def IsEmptyCell(self, row, col):
		return False

	def GetValue(self, row, col):
		entry = self.entries[row]
		return getattr(entry, self.colAttrs[col])

	def SetValue(self, row, col, value):
		pass

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent, data):
        wx.grid.Grid.__init__(self, parent, -1, wx.Point(0, 0), wx.Size(600, 600))
        tableBase = RelationTable(data)
        self.SetTable(tableBase) 

