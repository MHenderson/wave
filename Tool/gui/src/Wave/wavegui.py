import wx, sys, pickle, wx.aui, os
from exceptions import IOError
import Wave
from Wave import images, dbif, grid, MM2, error
from Wave.error import WaveIOError

##
# \todo A WaveSession should also contain metamodels.

class WaveSession():

    """Wave session class.
    
       A Wave session consists of a collection of Wave Relations. The
       collection of relations constitutes a model."""
    
    ##
    # \todo 'relations' member should be renamed 'model'.

    def __init__(self, relations = []):
        self.relations = relations

    ##
    # \todo Rename 'model'.

    def data(self):
        return self.relations

    ##
    # \todo Rename 'add_new_relation'.

    def add_new_table(self, relation):
        self.relations.append(Wave.grid.Relation(relation.table, relation.name))

class WaveNotebook(wx.aui.AuiNotebook):
    """Custom WAVE wxPython-Notebook class.
    
    """

    def __init__(self, parent):
        wx.aui.AuiNotebook.__init__(self, parent)

    def new_page(self, grid_table):
        page = wx.Panel(self)
        self.AddPage(page, grid_table.relation.name)
        Wave.grid.WaveGrid(page, grid_table)

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
#  \todo Design and implement a component to turn any dbif-style function
#        into an event handler. (e.g. dbif.join --> on_join)
#  \bug  Inconsistent behavior of session saving. On Windows, Wave can 
#        produce .wave files with a different format to those produced
#        on Linux.
#  \todo Implement row deletion for a specified row.
#  \bug  Closing the main window on Windows generates an error.
#  \todo Window title should incorporate name of currently open session.

class MainFrame(wx.Frame):
    """Custom WAVE top-level window class."""

    def __init__(self, parent, id):
        self.size = (600, 600)
        self.title = "WAVE (Whole Architecture Verification)"
        wx.Frame.__init__(self, parent, id, title = self.title, size = self.size)
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
        self.exit_menu_item = self.session_menu.Append(wx.NewId(), "E&xit\tCtrl-Q", "Exit")

    def init_models_menu(self):
        self.models_menu = wx.Menu()
        self.new_model_menu_item = self.models_menu.Append(wx.NewId(), "&New relation\tCtrl-N", "Add a new relation to the current model.")
        self.new_row_menu_item = self.models_menu.Append(wx.NewId(), "Add row\tCtrl-R", "Add row to the current relation.")
        self.delete_row_menu_item = self.models_menu.Append(wx.NewId(), "Delete row\tCtrl-X", "Delete row from the current relation.")

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
        self.menuBar.Append(self.session_menu, "&Session")
        self.menuBar.Append(self.models_menu, "&Model")
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
        selection = self.notebook.GetSelection()
        children = self.notebook.GetPage(selection).GetChildren()
        return children[0]

    def update_session(self):
        no_of_pages = self.notebook.GetPageCount()
        pages = [self.notebook.GetPage(i) for i in range(no_of_pages)]
        children = [page.GetChildren() for page in pages]
        grids = [child[0] for child in children]
        relations = [grid.grid_table.relation for grid in grids]
        self.session = WaveSession(relations)

    def on_open_session(self, event):
        wildcard = "Wave files (*.wave)|*.wave| " \
                   "All files (*.*)|*.* "
        dlg = wx.FileDialog(
                self, message = "Choose a file",
                defaultDir = os.getcwd(), 
                defaultFile = "",
                wildcard = wildcard,
                style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
        try:
            file = open(paths[0], 'rb')
        except IOError:
            raise WaveIOError
        dlg.Destroy()        
        self.session = pickle.load(file)
        relations = self.session.data()
        for relation in relations:
            grid_table = Wave.grid.WaveGridTable(relation)
            self.notebook.new_page(grid_table)
        file.close()

    def on_save_session(self, event):
        wildcard = "Wave files (*.wave)|*.wave| " \
                   "All files (*.*)|*.* "
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        dlg.SetFilterIndex(2)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
        try:
            file = open(path, 'wb')
        except IOError:
            raise WAVEIOError
        dlg.Destroy()
        self.update_session()
        pickle.dump(self.session, file)
        file.close()

    def on_close(self, event):
        self.Close(True)

    def on_new_row(self, event):
        grid = self.current_grid()
        grid.AppendRows()
        grid.ForceRefresh()

    def on_new_model(self, event):
        dialog_results = wx.TextEntryDialog(None, "Enter name for new relation:",'Relation name', 'New relation')
        if dialog_results.ShowModal() == wx.ID_OK:
            name = dialog_results.GetValue()
        dialog_results.Destroy()
        relation = Wave.grid.Relation([], name) 
        grid_table = Wave.grid.WaveGridTable(relation)
        self.session.add_new_table(relation)	
        self.notebook.new_page(grid_table)

    def on_delete_row(self, event):
        grid = self.current_grid()
        grid.DeleteRows()
        grid.ForceRefresh()

    def on_invert(self, event):
        current_grid = self.current_grid()
        current_grid_table = current_grid.grid_table
        result_name = '~' + current_grid.grid_table.relation.name
        result_grid_table = Wave.grid.apply_to_grid_tables(dbif.invert, current_grid_table, name = result_name)
        self.notebook.new_page(result_grid_table)       

    def on_closure(self, event):
        current_grid = self.current_grid()
        result_name = '^' + current_grid.grid_table.relation.name
        result_table = Wave.grid.apply_dbif_operation(dbif.close, current_grid)
        result_relation = Wave.grid.Relation(result_table, result_name)
        result_grid_table = Wave.grid.WaveGridTable(result_relation)
        self.notebook.new_page(result_grid_table)       

    def select_grid(self):
        no_of_pages = self.notebook.GetPageCount()
        pages = [self.notebook.GetPage(i) for i in range(no_of_pages)]
        children = [page.GetChildren() for page in pages]
        grids = [child[0] for child in children]
        choices = [grid.grid_table.relation.name for grid in grids]
        dialog_results = wx.SingleChoiceDialog ( None, 'Pick something....', 'Dialog Title', choices )
        if dialog_results.ShowModal() == wx.ID_OK:
            position = dialog_results.GetSelection()
        dialog_results.Destroy()	    
        return grids[position]

    def on_join(self, event):
        grid1 = self.select_grid()
        grid2 = self.select_grid()
        result_name = grid1.grid_table.relation.name + '.' + grid2.grid_table.relation.name	
        result_table = Wave.grid.apply_dbif_operation(dbif.join, grid1, grid2)
        result_relation = Wave.grid.Relation(result_table, result_name)
        result_grid_table = Wave.grid.WaveGridTable(result_relation)
        self.notebook.new_page(result_grid_table)

    def on_diff(self, event):
        grid1 = self.select_grid()
        grid2 = self.select_grid()
        result_name = grid1.grid_table.relation.name + ' - ' + grid2.grid_table.relation.name	
        result_table = Wave.grid.apply_dbif_operation(dbif.diff, grid1, grid2)
        result_relation = Wave.grid.Relation(result_table, result_name)
        result_grid_table = Wave.grid.WaveGridTable(result_relation)
        self.notebook.new_page(result_grid_table)

    def on_dr(self, event):
        grid1 = self.select_grid()
        grid2 = self.select_grid()
        grid3 = self.select_grid()
        result_name = 'dangling requires'
        result_table = Wave.grid.apply_dbif_operation(MM2.dr, grid1, grid2, grid3)
        result_relation = Wave.grid.Relation(result_table, result_name)
        result_grid_table = Wave.grid.WaveGridTable(result_relation)
        self.notebook.new_page(result_grid_table)

def main():
    app = WaveApp()
    app.MainLoop()
    return 0

if __name__ == '__main__':
    sys.exit(main())

