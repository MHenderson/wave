#!/usr/bin/env python
 
import wx, images, simplegrid

MAIN_FRAME_SIZE = (600, 600)
MAIN_FRAME_TITLE = "WAVe (Whole Architecture Verification)"

data = []

class WaveApp(wx.App):
    """Custom WAVE wxPython-application class."""

    def __init__(self, redirect = False, filename = None, useBestVisual = False, clearSigInt = True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
	# image = wx.Image("wave-logo.bmp", wx.BITMAP_TYPE_BMP)
	# bmp = image.ConvertToBitmap()
	# wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 1000, None, -1)
	# wx.Yield()
	frame = MainFrame(None, -1)
        frame.Show(1)
	self.SetTopWindow(frame)
        return True

class MainFrame(wx.Frame):
    """Custom WAVE top-level window class."""

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = MAIN_FRAME_TITLE, size = MAIN_FRAME_SIZE)
        self.init_panel()
        self.init_statusbar()
        self.init_toolbar()
        self.init_menus()
	self.init_event_binding()

    def init_panel(self):
        self.panel = wx.Panel(self)
	
    def init_statusbar(self):
        self.statusBar = self.CreateStatusBar()

    def init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        self.new_model_toolbar_item = self.toolbar.AddSimpleTool(wx.NewId(), images.getNewBitmap(), "New", "Long help for 'New'")
        self.toolbar.Realize()

    def init_menus(self):
	self.init_models_menu()
	self.init_metamodels_menu()
	self.init_scripts_menu()
	self.init_menubar()

    def init_models_menu(self):
        self.models_menu = wx.Menu()
        self.new_model_menu_item = self.models_menu.Append(wx.NewId(), "&New\tCtrl-N", "New")
        self.models_menu.Append(wx.NewId(), "&Open", "Open")
        self.models_menu.Append(wx.NewId(), "&Save", "Save")
        self.new_row_menu_item = self.models_menu.Append(wx.NewId(), "Add row\tCtrl-R", "Add row")
        self.exit_menu_item = self.models_menu.Append(wx.NewId(), "E&xit\tCtrl-Q", "Exit")

    def init_metamodels_menu(self):
        self.metamodels_menu = wx.Menu()
        self.metamodels_menu.Append(wx.NewId(), "&Import", "Import")
        self.metamodels_menu.Append(wx.NewId(), "&Export", "Export")
        self.metamodels_menu.AppendSeparator()
        self.metamodels_menu.Append(wx.NewId(), "&MM2 (Current metamodel)", "Display Options")
        
    def init_scripts_menu(self):
        self.scripts_menu = wx.Menu()
        self.scripts_menu.Append(wx.NewId(), "d&r", "Dangling requires")
        self.scripts_menu.Append(wx.NewId(), "d&s", "Dangling supplies")
        self.scripts_menu.AppendSeparator()
        self.scripts_menu.Append(wx.NewId(), "Export HTML report", "")

    def init_menubar(self):
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.models_menu, "&Models")
        self.menuBar.Append(self.metamodels_menu, "M&eta-models")
        self.menuBar.Append(self.scripts_menu, "&Scripts")       
        self.SetMenuBar(self.menuBar)

    def init_event_binding(self):
        self.Bind(wx.EVT_MENU, self.OnCloseMe, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.OnNewRow, self.new_row_menu_item)
        self.Bind(wx.EVT_MENU, self.OnNewModel, self.new_model_menu_item)
	self.Bind(wx.EVT_TOOL, self.OnNewModel, self.new_model_toolbar_item)

    # Event-handlers

    def OnCloseMe(self, event):
        self.Close(True)

    def OnNewRow(self, event):
	self.grid.AppendRows()
	self.grid.ForceRefresh()

    def OnNewModel(self, event):
	self.grid = simplegrid.SimpleGrid(self.panel, data)

if __name__ == '__main__':
    app = WaveApp()
    app.MainLoop()

