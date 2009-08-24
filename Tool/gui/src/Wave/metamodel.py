import wx
import Wave
from Wave import handlers

class Function():

    def __init__(self, function, fix = False, symbol = False, name = False):
        self.function = function
        self.fix = fix
        self.symbol = symbol
        self.name = name
        self.handler = self.apply_strategy()

    def get_function(self):
        return self.function

    def get_handler(self):
        return self.handler

    def apply_strategy(self):
        nargs = self.function.func_code.co_argcount
        if nargs == 1:
            return self.unary_strategy()
        elif nargs == 2:
            return self.binary_strategy()
        elif nargs == 3:
            return self.ternary_strategy()
        else:
            pass

    def unary_strategy(self):
        if ((self.fix == 'pre') and self.symbol):
            return Wave.handlers.UnaryPrefixOperatorToCurrentPage(self.function, self.symbol)
        else:
            raise Wave.exceptions.WaveMissingCallStrategy

    def binary_strategy(self):
        if ((self.fix == 'in') and self.symbol):
            return Wave.handlers.BinaryInfixOperatorToSelectedPages(self.function, self.symbol)
        elif ((self.fix == False) and self.name):
            return Wave.handlers.BinaryFunctionToSelectedPages(self.function, self.name)
        else:
            raise Wave.exceptions.WaveMissingCallStrategy            

    def ternary_strategy(self):
        if ((self.fix == False) and self.name):
            return Wave.handlers.TernaryFunctionToSelectedPages(self.function, self.name)
        else:
            raise Wave.exceptions.WaveMissingCallStrategy            

class Metamodel():

    def __init__(self):
        self.functions_names_map = {}

    def add_function(self, function, name, long_name):
        self.functions_names_map[function] = {'name': name, 'long_name': long_name}

    def get_name(self, function):
        return self.functions_names_map[function]['name']

    def get_long_name(self, function):
        return self.functions_names_map[function]['long_name']

    def functions(self):
        return self.functions_names_map.keys()

class MetamodelMenu():

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
            self.frame.Bind(wx.EVT_MENU, self.create_handler(self.frame, wave_function), self.frame.mm_sub_menu_items[name])

