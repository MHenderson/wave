import wx, sys, pickle
import Wave
from Wave import images, dbif, grid, MM2

MAIN_FRAME_SIZE = (600, 600)
MAIN_FRAME_TITLE = "WAVe (Whole Architecture Verification)"

class WaveSession():

    """Wave session class.
    
       A Wave session consists of a dictionary of name/table pairs. Each pair
       corresponds to a named-table in the Wave gui.
    """

    def __init__(self, tables = {}):
        self.tables = tables

    def data(self):
        return self.tables

    def add_new_table(self, table = [], name = ''):
        self.tables[name] = table

class WaveNotebook(wx.Notebook):
    """Custom WAVE wxPython-Notebook class.
    
       A WaveNotebook extends the wx.Notebook by a collection of pages objects.
    """

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.pages = []

    def new_page(self, table):
        self.pages.append(wx.Panel(self))
        self.AddPage(self.pages[-1], table.name)
        self.grid = Wave.grid.WaveGrid(self.pages[-1], table)

## Custom WAVE wxPython-application class.
#
#  \todo Implement a splash-screen.

class WaveApp(wx.App):
    """Custom WAVE wxPython-application class."""

    def __init__(self, redirect = False, filename = None, useBestVisual = False, clearSigInt = True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)

    def OnInit(self):
        frame = MainFrame(None, -1)
        frame.Show(1)
        self.SetTopWindow(frame)
        return True

## Custom WAVE top-level window class.
#
#  \bug  Modifying a WaveGrid object has no effect on the underlying 
#        WaveSession object. Hence session saving is broken.

class MainFrame(wx.Frame):
    """Custom WAVE top-level window class."""

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title = MAIN_FRAME_TITLE, size = MAIN_FRAME_SIZE)
        self.init_session()
        self.init_panel()
        self.init_notebook()
        self.init_statusbar()
        self.init_toolbar()
        self.init_menus()
        self.init_event_binding()

    def init_session(self):
        self.session = WaveSession()

    def init_panel(self):
        self.panel = wx.Panel(self)

    def init_notebook(self):
        self.notebook = WaveNotebook(self.panel)
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

    def init_statusbar(self):
        self.statusBar = self.CreateStatusBar()

    def init_toolbar(self):
        self.toolbar = self.CreateToolBar()
        self.new_model_toolbar_item = self.toolbar.AddSimpleTool(wx.NewId(), Wave.images.getNewBitmap(), "New", "Long help for 'New'")
        self.toolbar.Realize()

    def init_menus(self):
        self.init_session_menu()
        self.init_models_menu()
        self.init_metamodels_menu()
        self.init_operations_menu()
        self.init_scripts_menu()
        self.init_menubar()

    def init_session_menu(self):
        self.session_menu = wx.Menu()
        self.open_session_menu_item = self.session_menu.Append(wx.NewId(), "&Open", "Open")
        self.save_session_menu_item = self.session_menu.Append(wx.NewId(), "&Save", "Save")

    def init_models_menu(self):
        self.models_menu = wx.Menu()
        self.new_model_menu_item = self.models_menu.Append(wx.NewId(), "&New\tCtrl-N", "New")
        self.models_menu.Append(wx.NewId(), "&Open", "Open")
        self.models_menu.Append(wx.NewId(), "&Save", "Save")
        self.new_row_menu_item = self.models_menu.Append(wx.NewId(), "Add row\tCtrl-R", "Add row")
        self.delete_row_menu_item = self.models_menu.Append(wx.NewId(), "Delete row\tCtrl-X", "Delete row")
        self.exit_menu_item = self.models_menu.Append(wx.NewId(), "E&xit\tCtrl-Q", "Exit")

    def init_metamodels_menu(self):
        self.metamodels_menu = wx.Menu()
        self.metamodels_menu.Append(wx.NewId(), "&Import", "Import")
        self.metamodels_menu.Append(wx.NewId(), "&Export", "Export")
        self.metamodels_menu.AppendSeparator()
        self.metamodels_menu.Append(wx.NewId(), "&MM2 (Current metamodel)", "Display Options")

    def init_operations_menu(self):
        self.operations_menu = wx.Menu()
        self.invert_menu_item = self.operations_menu.Append(wx.NewId(), "Invert\tCtrl-`", "Invert")
        self.closure_menu_item = self.operations_menu.Append(wx.NewId(), "Closure", "Transitive closure.")
        self.join_menu_item = self.operations_menu.Append(wx.NewId(), "Join", "Join.")
        self.diff_menu_item = self.operations_menu.Append(wx.NewId(), "Diff", "Difference.")


    def init_scripts_menu(self):
        self.scripts_menu = wx.Menu()
        self.dr_menu_item = self.scripts_menu.Append(wx.NewId(), "d&r", "Dangling requires")
        self.scripts_menu.Append(wx.NewId(), "d&s", "Dangling supplies")
        self.scripts_menu.AppendSeparator()
        self.scripts_menu.Append(wx.NewId(), "Export HTML report", "")

    def init_menubar(self):
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.session_menu, "&Sessions")
        self.menuBar.Append(self.models_menu, "&Models")
        self.menuBar.Append(self.metamodels_menu, "M&eta-models")
        self.menuBar.Append(self.operations_menu, "&Operations")       
        self.menuBar.Append(self.scripts_menu, "Sc&ripts")       
        self.SetMenuBar(self.menuBar)

    def init_event_binding(self):
        self.Bind(wx.EVT_MENU, self.on_close, self.exit_menu_item)
        self.Bind(wx.EVT_MENU, self.on_new_row, self.new_row_menu_item)
        self.Bind(wx.EVT_MENU, self.on_new_model, self.new_model_menu_item)
        self.Bind(wx.EVT_TOOL, self.on_new_model, self.new_model_toolbar_item)
        self.Bind(wx.EVT_MENU, self.on_delete_row, self.delete_row_menu_item)
        self.Bind(wx.EVT_MENU, self.on_invert, self.invert_menu_item)
        self.Bind(wx.EVT_MENU, self.on_closure, self.closure_menu_item)
        self.Bind(wx.EVT_MENU, self.on_join, self.join_menu_item)
        self.Bind(wx.EVT_MENU, self.on_diff, self.diff_menu_item)
        self.Bind(wx.EVT_MENU, self.on_dr, self.dr_menu_item)
        self.Bind(wx.EVT_MENU, self.on_open_session, self.open_session_menu_item)
        self.Bind(wx.EVT_MENU, self.on_save_session, self.save_session_menu_item)

    def current_grid(self):
        children = self.notebook.GetCurrentPage().GetChildren()
        return children[0]

    def update_session(self):
        no_of_pages = self.notebook.GetPageCount()
        pages = [self.notebook.GetPage(i) for i in range(no_of_pages)]
        children = [page.GetChildren() for page in pages]
        grids = [child[0] for child in children]
        names = [grid.name for grid in grids]
        tables = [grid.GetTable().entries for grid in grids]
        session_data = dict(zip(names, tables))
        self.session = WaveSession(session_data)

    def on_open_session(self, event):
        file = open(r'/home/matthew/Desktop/session.wave', 'rb')
        self.session = pickle.load(file)
        data = self.session.data()
        for name, table in data.iteritems():
            grid_table = Wave.grid.WaveGridTable(table, name)
            self.session.add_new_table(table, name)	
            self.notebook.new_page(grid_table)
        file.close()

    def on_save_session(self, event):
        self.update_session()
        file = open(r'/home/matthew/Desktop/session.wave', 'wb')
        pickle.dump(self.session, file)
        file.close()

    def on_close(self, event):
        self.Close(True)

    def on_new_row(self, event):
        grid = self.current_grid()
        grid.AppendRows()
        grid.ForceRefresh()

    def on_new_model(self, event):
        dialog_results = wx.TextEntryDialog(None, "Enter name for new relation table:",'Relation name', 'New relation')
        if dialog_results.ShowModal() == wx.ID_OK:
            name = dialog_results.GetValue()
        dialog_results.Destroy()
        table = [] 
        grid_table = Wave.grid.WaveGridTable([], name)
        self.session.add_new_table(table, name)	
        self.notebook.new_page(grid_table)

    def on_delete_row(self, event):
        grid = self.current_grid()
        grid.DeleteRows()
        grid.ForceRefresh()

    def on_invert(self, event):
        grid = self.current_grid()
        name_ = '~' + grid.name
        r_table = Wave.grid.apply_dbif_operation(dbif.invert, grid, name = name_)
        self.notebook.new_page(r_table)       

    def on_closure(self, event):
        grid = self.current_grid()
        name_ = '^' + grid.name
        r_table = Wave.grid.apply_dbif_operation(dbif.close, grid, name = name_)
        self.notebook.new_page(r_table)       

    def select_grid(self):
        no_of_pages = self.notebook.GetPageCount()
        pages = [self.notebook.GetPage(i) for i in range(no_of_pages)]
        children = [page.GetChildren() for page in pages]
        grids = [child[0] for child in children]
        choices = [grid.name for grid in grids]
        dialog_results = wx.SingleChoiceDialog ( None, 'Pick something....', 'Dialog Title', choices )
        if dialog_results.ShowModal() == wx.ID_OK:
            position = dialog_results.GetSelection()
        dialog_results.Destroy()	    
        return grids[position]

    def on_join(self, event):
        grid1 = self.select_grid()
        grid2 = self.select_grid()
        table_name = grid1.name + '.' + grid2.name	
        table = Wave.grid.apply_dbif_operation(dbif.join, grid1, grid2, name = table_name)
        self.notebook.new_page(table)

    def on_diff(self, event):
        grid1 = self.select_grid()
        grid2 = self.select_grid()
        table_name = grid1.name + ' - ' + grid2.name	
        table = Wave.grid.apply_dbif_operation(dbif.diff, grid1, grid2, name = table_name)
        self.notebook.new_page(table)

    def on_dr(self, event):
        grid1 = self.select_grid()
        grid2 = self.select_grid()
        grid3 = self.select_grid()
        table_name = 'dangling requires'
        table = Wave.grid.apply_dbif_operation(MM2.dr, grid1, grid2, grid3, name = table_name)
        self.notebook.new_page(table)

def main():
    app = WaveApp()
    app.MainLoop()
    return 0

if __name__ == '__main__':
    sys.exit(main())

