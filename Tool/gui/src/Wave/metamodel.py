import wx
import MM2
import Wave
from Wave import handlers

def on_dr(self, event):
    Wave.handlers.ternary_function_to_selected_pages(self, MM2.DR, 'dr')

def on_ds(self, event):
    Wave.handlers.binary_function_to_selected_pages(self, MM2.DS, 'ds')

class WaveMetamodelMenu():

    def __init__(self, frame):
        self.frame = frame
        self.init_menus()
        self.bind_handlers()

    def init_menus(self):
        self.frame.scripts_menu = wx.Menu()
        self.frame.dr_menu_item = self.frame.scripts_menu.Append(wx.NewId(), "d&r", "Dangling requires")
        self.frame.ds_menu_item = self.frame.scripts_menu.Append(wx.NewId(), "d&s", "Dangling supplies")
        self.frame.menuBar.Append(self.frame.scripts_menu, "MM2")  

    def bind_handlers(self):
        self.frame.Bind(wx.EVT_MENU, on_dr, self.frame.dr_menu_item)
        self.frame.Bind(wx.EVT_MENU, on_ds, self.frame.ds_menu_item)

