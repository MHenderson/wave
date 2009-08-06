#!/usr/bin/env python
 
import wx, images, simplegrid

MAIN_FRAME_SIZE = (600, 600)
MAIN_FRAME_TITLE = "WAVe (Whole Architecture Verification)"

data = [("A", "B"), ("X", "Y")]

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
        self.init_menubar()
	self.init_grid()

        # Event-handling

        self.Bind(wx.EVT_MENU, self.OnCloseMe, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.OnNewRow, self.new_row_menu_item)

    # Initialization

    def init_panel(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('White')

    def init_grid(self):
	self.grid = simplegrid.SimpleGrid(self.panel, data)	

    def init_statusbar(self):
        self.statusBar = self.CreateStatusBar()

    def init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        self.toolbar.AddSimpleTool(wx.NewId(), images.getNewBitmap(), "New", "Long help for 'New'")
        self.toolbar.Realize()

    def init_menubar(self):
        # Models Menu
        models_menu = wx.Menu()
        models_menu.Append(wx.NewId(), "&Open", "Open")
        models_menu.Append(wx.NewId(), "&Save", "Save")
        self.new_row_menu_item = models_menu.Append(wx.NewId(), "Add row", "Add row")
        self.exit_menu_item = models_menu.Append(wx.NewId(), "E&xit", "Exit")
        # Metamodels Menu
        metamodels_menu = wx.Menu()
        metamodels_menu.Append(wx.NewId(), "&Import", "Import")
        metamodels_menu.Append(wx.NewId(), "&Export", "Export")
        metamodels_menu.AppendSeparator()
        metamodels_menu.Append(wx.NewId(), "&MM2 (Current metamodel)", "Display Options")
        # Scripts Menu
        scripts_menu = wx.Menu()
        scripts_menu.Append(wx.NewId(), "d&r", "Dangling requires")
        scripts_menu.Append(wx.NewId(), "d&s", "Dangling supplies")
        scripts_menu.AppendSeparator()
        scripts_menu.Append(wx.NewId(), "Export HTML report", "")
        # Menu Bar
        menuBar = wx.MenuBar()
        menuBar.Append(models_menu, "&Models")
        menuBar.Append(metamodels_menu, "M&eta-models")
        menuBar.Append(scripts_menu, "&Scripts")       
        self.SetMenuBar(menuBar)

    # Event-handlers

    def OnCloseMe(self, event):
        self.Close(True)

    def OnNewRow(self, event):
	self.grid.AppendRows()
	self.grid.ForceRefresh()

if __name__ == '__main__':
    app = WaveApp()
    app.MainLoop()

