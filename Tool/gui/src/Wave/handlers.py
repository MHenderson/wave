import Wave
from Wave import grid

##
#
# \todo These aren't 'handlers'. They are 'function-call strategies'. Use
#       suitable naming.

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

