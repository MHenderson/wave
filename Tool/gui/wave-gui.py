#!/usr/bin/env python
 
import wx
import images

MAIN_FRAME_SIZE = (600, 600)
MAIN_FRAME_TITLE = "WAVe (Whole Architecture Verification)"

class WaveApp(wx.App):

    def __init__(self, redirect = False, filename = None, useBestVisual = False, clearSigInt = True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        return True

class MainFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = MAIN_FRAME_TITLE, size = MAIN_FRAME_SIZE)
        panel = wx.Panel(self)
        panel.SetBackgroundColour('White')
        statusBar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        toolbar.AddSimpleTool(wx.NewId(), images.getNewBitmap(), "New", "Long help for 'New'")
        toolbar.Realize()
        menuBar = wx.MenuBar()
        models_menu = wx.Menu()
        models_menu.Append(wx.NewId(), "&Open", "Open")
        models_menu.Append(wx.NewId(), "&Save", "Save")
        models_menu.Append(wx.NewId(), "E&xit", "Exit")
        menuBar.Append(models_menu, "&Models")
        metamodels_menu = wx.Menu()
        metamodels_menu.Append(wx.NewId(), "&Import", "Copy")
        metamodels_menu.Append(wx.NewId(), "&Export", "Copy")
        metamodels_menu.AppendSeparator()
        metamodels_menu.Append(wx.NewId(), "&MM2 (Current metamodel)", "Display Options")
        menuBar.Append(metamodels_menu, "M&eta-models")
        scripts_menu = wx.Menu()
        scripts_menu.Append(wx.NewId(), "d&r", "Dangling requires")
        scripts_menu.Append(wx.NewId(), "d&s", "Dangling supplies")
        scripts_menu.AppendSeparator()
        scripts_menu.Append(wx.NewId(), "Export HTML report", "")
        menuBar.Append(scripts_menu, "&Scripts")
        self.SetMenuBar(menuBar)

if __name__ == '__main__':
    app = WaveApp()
    frame = MainFrame(None, -1)
    frame.Show(1)
    app.MainLoop()
