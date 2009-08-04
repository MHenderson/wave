import wx, generictable

data = [["A", "F"], ["K", "O"], 
        ["B", "G"], ["L", "P"],
        ["C", "H"], ["M", "U"],
        ["D", "I"], ["N", "V"],
        ["E", "J"]]
            
colLabels = ["XXX", "YYY"]
rowLabels = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1, wx.Point(0, 0), wx.Size(600, 600))
        tableBase = generictable.GenericTable(data, rowLabels, colLabels)
        self.SetTable(tableBase) 

