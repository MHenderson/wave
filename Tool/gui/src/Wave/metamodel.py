import wx
import MM2
import Wave
from Wave import handlers

class WaveMetamodelMenu():

    def __init__(self, frame):
        self.frame = frame
        self.init_menus()
        self.bind_handlers()

    def init_menus(self):
        self.frame.mm2_sub_menu = wx.Menu()
        self.frame.dr_menu_item = self.frame.mm2_sub_menu.Append(wx.NewId(), "d&r", "Dangling requires")
        self.frame.ds_menu_item = self.frame.mm2_sub_menu.Append(wx.NewId(), "d&s", "Dangling supplies")
        self.frame.metamodels_menu.AppendSeparator()
        self.frame.metamodels_menu.AppendMenu(-1, "MM2", self.frame.mm2_sub_menu)  
            
    def on_dr(self, event):
        Wave.handlers.ternary_function_to_selected_pages(self.frame, MM2.DR, 'dr')
        
    def on_ds(self, event):
        Wave.handlers.binary_function_to_selected_pages(self.frame, MM2.DS, 'ds')

    def bind_handlers(self):
        self.frame.Bind(wx.EVT_MENU, self.on_dr, self.frame.dr_menu_item)
        self.frame.Bind(wx.EVT_MENU, self.on_ds, self.frame.ds_menu_item)

