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

    def bind_handlers(self):
        self.frame.Bind(wx.EVT_MENU, self.frame.on_dr, self.frame.dr_menu_item)
        self.frame.Bind(wx.EVT_MENU, self.frame.on_ds, self.frame.ds_menu_item)

