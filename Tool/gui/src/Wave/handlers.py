import Wave
from Wave import grid

def unary_prefix_operator_to_current_page(frame, operator, prefix):
    current_page_index = frame.notebook.GetSelection()
    result_name = prefix + frame.notebook.GetPageText(current_page_index)
    current_grid_table = frame.current_grid_table()        
    result_grid_table = Wave.grid.apply_to_grid_tables(operator, current_grid_table)
    frame.notebook.new_page(result_grid_table, result_name)

def binary_infix_operator_to_selected_pages(frame, operator, infix):       
    page_index_1 = frame.select_page_index()
    page_index_2 = frame.select_page_index()
    result_name = frame.notebook.GetPageText(page_index_1) + infix + frame.notebook.GetPageText(page_index_2)
    grid_table_1 = frame.get_grid_table(page_index_1)
    grid_table_2 = frame.get_grid_table(page_index_2)
    result_grid_table = Wave.grid.apply_to_grid_tables(operator, grid_table_1, grid_table_2)
    frame.notebook.new_page(result_grid_table, result_name)

def binary_function_to_selected_pages(frame, function, name):
    page_index_1 = frame.select_page_index()
    page_index_2 = frame.select_page_index()
    name_1 = frame.notebook.GetPageText(page_index_1)
    name_2 = frame.notebook.GetPageText(page_index_2)
    grid_table_1 = frame.get_grid_table(page_index_1)
    grid_table_2 = frame.get_grid_table(page_index_2)
    result_name = name + '(' + name_1 + ', ' + name_2 + ')'
    result_grid_table = Wave.grid.apply_to_grid_tables(function, grid_table_1, grid_table_2)
    frame.notebook.new_page(result_grid_table, result_name)

def ternary_function_to_selected_pages(frame, function, name):
    page_index_1 = frame.select_page_index()
    page_index_2 = frame.select_page_index()
    page_index_3 = frame.select_page_index()
    name_1 = frame.notebook.GetPageText(page_index_1)
    name_2 = frame.notebook.GetPageText(page_index_2)
    name_3 = frame.notebook.GetPageText(page_index_3)
    grid_table_1 = frame.get_grid_table(page_index_1)
    grid_table_2 = frame.get_grid_table(page_index_2)
    grid_table_3 = frame.get_grid_table(page_index_3)
    result_name = name + '(' + name_1 + ', ' + name_2 + ', ' + name_3 + ')'
    result_grid_table = Wave.grid.apply_to_grid_tables(function, grid_table_1, grid_table_2, grid_table_3)
    frame.notebook.new_page(result_grid_table, result_name)


class HandlingStrategy():

    def __init__(self, function):
        self.function = function

    def __call__(self, infix = False):
        nargs = self.function.func_code.co_argcount
        if nargs == 1:
            return Wave.handlers.unary_prefix_operator_to_current_page
        elif nargs == 2:
            if infix:
                return Wave.handlers.binary_infix_operator_to_selected_pages
            else:
                return Wave.handlers.binary_function_to_selected_pages
        elif nargs == 3:
            return Wave.handlers.ternary_function_to_selected_pages
        else:
            pass

