import wx
import Wave
from Wave import handlers

class Function():

    def __init__(self, function, handler):
        self.function = function
        self.handler = handler

    def get_function(self):
        return self.function

    def get_handler(self):
        return self.handler

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

    def __init__(self, frame, metamodel):
        self.frame = frame
        self.metamodel = metamodel
        self.init_menus()
        self.bind_handlers()

    def create_handler(self, frame, wave_function):
        def on(event):
            wave_function.handler(frame, wave_function.get_function(), self.metamodel.get_name(wave_function))
        return on

    def init_menus(self):
        self.frame.mm_sub_menu = wx.Menu()
        self.frame.mm_sub_menu_items = {}
        for wave_function in self.metamodel.functions():
            name = self.metamodel.get_name(wave_function)
            long_name = self.metamodel.get_long_name(wave_function)
            self.frame.mm_sub_menu_items[name] = self.frame.mm_sub_menu.Append(wx.NewId(), name, long_name)
        self.frame.metamodels_menu.AppendSeparator()
        self.frame.metamodels_menu.AppendMenu(-1, 'MM2', self.frame.mm_sub_menu)  

    def bind_handlers(self):
        for wave_function in self.metamodel.functions():
            name = self.metamodel.get_name(wave_function)
            self.frame.Bind(wx.EVT_MENU, self.create_handler(self.frame, wave_function), self.frame.mm_sub_menu_items[name])

