import wx, wx.grid
           
class Relation():

    """Basic representation of relations."""

    def __init__(self, table = []):
        self.table = table

    def __delitem__(self, index):
        del self.table[index]

class WaveGridTable(wx.grid.PyGridTableBase, Relation):

    """Custom WAVE GridTable class.
    
       Adapts a Wave Table for use as a grid table.
    """
    
    def __init__(self, relation):
        wx.grid.PyGridTableBase.__init__(self)
        self.relation = relation

    def GetNumberRows(self):
        return len(self.relation.table)

    def GetNumberCols(self):
        return 2

    def GetColLabelValue(self, col):
        return col

    def GetRowLabelValue(self, row):
        return row

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.relation.table[row][col]

    def SetValue(self, row, col, value):
        current_tuple = self.relation.table[row]
        self.relation.table[row] = current_tuple[:col] + (value,) + current_tuple[col+1:]

    def AppendRows(self, num_of_rows = 1):
        self.relation.table.append((0,0))

    def DeleteRows(self, pos = 0, numRows = 1, updateLabels = False):
        del self.relation[pos]

class WaveGrid(wx.grid.Grid):

    def __init__(self, parent, grid_table):
        wx.grid.Grid.__init__(self, parent, -1, wx.Point(0, 0), wx.Size(600, 520))
        self.grid_table = grid_table
        self.SetTable(self.grid_table) 

    def AppendRows(self, num_of_rows = 1):
        self.GetTable().AppendRows()
        self.SetTable(self.GetTable()) 

    def DeleteRows(self, pos = 0, numRows = 1, updateLabels = False):
        self.GetTable().DeleteRows(pos, numRows, updateLabels)
        self.SetTable(self.GetTable()) 


## apply_dbif_operation
#
#  Applies a dbif operation to a collection of WaveGrid objects.
#
#  \todo Refactor into two components - one which handles Relations and
#        another which, for convenience, handles grids.

def apply_dbif_operation(operation, *grids):
    grid_tables = [grid.GetTable() for grid in grids]
    relations = [grid_table.relation for grid_table in grid_tables]
    relation_tables = [relation.table for relation in relations]
    result_table = operation(*relation_tables)
    return result_table

def apply_to_relations(operation, *relations):
    relation_tables = [relation.table for relation in relations]
    result_table = operation(*relation_tables)
    result_relation = Relation(result_table)
    return result_relation

def apply_to_grid_tables(operation, *grid_tables):
    relations = [grid_table.relation for grid_table in grid_tables]
    result_relation = apply_to_relations(operation, *relations)
    result_grid_table = WaveGridTable(result_relation)
    return result_grid_table


class UnaryPrefixOperatorToCurrentPage:

    def __init__(self, operator, prefix):
        self.operator = operator
        self.prefix = prefix

    def __call__(self, frame):
        current_page_index = frame.notebook.GetSelection()
        result_name = self.prefix + frame.notebook.GetPageText(current_page_index)
        current_grid_table = frame.current_grid_table()        
        result_grid_table = Wave.grid.apply_to_grid_tables(self.operator, current_grid_table)
        frame.notebook.new_page(result_grid_table, result_name)

class BinaryInfixOperatorToSelectedPages: 

    def __init__(self, operator, infix):
        self.operator = operator
        self.infix = infix

    def __call__(self, frame):
        page_index_1 = frame.select_page_index()
        page_index_2 = frame.select_page_index()
        result_name = frame.notebook.GetPageText(page_index_1) + self.infix + frame.notebook.GetPageText(page_index_2)
        grid_table_1 = frame.get_grid_table(page_index_1)
        grid_table_2 = frame.get_grid_table(page_index_2)
        result_grid_table = Wave.grid.apply_to_grid_tables(self.operator, grid_table_1, grid_table_2)
        frame.notebook.new_page(result_grid_table, result_name)

class BinaryFunctionToSelectedPages:

    def __init__(self, function, name):
        self.function = function
        self.name = name

    def __call__(self, frame):
        page_index_1 = frame.select_page_index()
        page_index_2 = frame.select_page_index()
        name_1 = frame.notebook.GetPageText(page_index_1)
        name_2 = frame.notebook.GetPageText(page_index_2)
        grid_table_1 = frame.get_grid_table(page_index_1)
        grid_table_2 = frame.get_grid_table(page_index_2)
        result_name = self.name + '(' + name_1 + ', ' + name_2 + ')'
        result_grid_table = Wave.grid.apply_to_grid_tables(self.function, grid_table_1, grid_table_2)
        frame.notebook.new_page(result_grid_table, result_name)

class TernaryFunctionToSelectedPages:

    def __init__(self, function, name):
        self.function = function 
        self.name = name

    def __call__(self, frame):
        page_index_1 = frame.select_page_index()
        page_index_2 = frame.select_page_index()
        page_index_3 = frame.select_page_index()
        name_1 = frame.notebook.GetPageText(page_index_1)
        name_2 = frame.notebook.GetPageText(page_index_2)
        name_3 = frame.notebook.GetPageText(page_index_3)
        grid_table_1 = frame.get_grid_table(page_index_1)
        grid_table_2 = frame.get_grid_table(page_index_2)
        grid_table_3 = frame.get_grid_table(page_index_3)
        result_name = self.name + '(' + name_1 + ', ' + name_2 + ', ' + name_3 + ')'
        result_grid_table = Wave.grid.apply_to_grid_tables(self.function, grid_table_1, grid_table_2, grid_table_3)
        frame.notebook.new_page(result_grid_table, result_name)


class FunctionWithCallStrategy():

    def __init__(self, function):
        self.function = function
        self.handler = self.apply_strategy()
        
    def get_handler(self):
        return self.handler

    def apply_strategy(self):
        nargs = self.function.nargs()
        if nargs == 1:
            return self.unary_strategy()
        elif nargs == 2:
            return self.binary_strategy()
        elif nargs == 3:
            return self.ternary_strategy()
        else:
            pass

    def unary_strategy(self):
        if ((self.function.fix == 'pre') and self.function.symbol):
            return UnaryPrefixOperatorToCurrentPage(self.function, self.function.symbol)
        else:
            raise Wave.exceptions.WaveMissingCallStrategy

    def binary_strategy(self):
        if ((self.function.fix == 'in') and self.function.symbol):
            return BinaryInfixOperatorToSelectedPages(self.function, self.function.symbol)
        elif ((self.function.fix == False) and self.function.name):
            return BinaryFunctionToSelectedPages(self.function, self.function.name)
        else:
            raise Wave.exceptions.WaveMissingCallStrategy            

    def ternary_strategy(self):
        if ((self.function.fix == False) and self.function.name):
            return TernaryFunctionToSelectedPages(self.function, self.function.name)
        else:
            raise Wave.exceptions.WaveMissingCallStrategy 


##
# \todo This Menu class ought not to belong to the metamodel module.

class Menu():

    def __init__(self, frame, metamodel, name):
        self.frame = frame
        self.metamodel = metamodel
        self.name = name
        self.init_menus()
        self.bind_handlers()

    def create_handler(self, frame, wave_function):
        def on(event):
            wave_function.handler(frame)
        return on

    def init_menus(self):
        self.frame.mm_sub_menu = wx.Menu()
        self.frame.mm_sub_menu_items = {}
        for wave_function in self.metamodel.functions():
            name = self.metamodel.get_name(wave_function)
            long_name = self.metamodel.get_long_name(wave_function)
            self.frame.mm_sub_menu_items[name] = self.frame.mm_sub_menu.Append(wx.NewId(), name, long_name)
        self.frame.metamodels_menu.AppendSeparator()
        self.frame.metamodels_menu.AppendMenu(-1, self.name, self.frame.mm_sub_menu)  

    def bind_handlers(self):
        for wave_function in self.metamodel.functions():
            name = self.metamodel.get_name(wave_function)
            function = FunctionWithCallStrategy(wave_function)
            handler = self.create_handler(self.frame, function)
            self.frame.Bind(wx.EVT_MENU, handler, self.frame.mm_sub_menu_items[name])        

