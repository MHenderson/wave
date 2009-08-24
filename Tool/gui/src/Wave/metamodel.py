import wx
import MM2
import Wave
from Wave import handlers

class WaveMetamodelFunction():

    def __init__(self, function, name, handler, long_name):
        self.function = function
        self.name = name
        self.handler = handler
        self.long_name = long_name

class WaveMetamodel():

    def __init__(self, name, functions):
        self.name = name
        self.functions = functions

DR = WaveMetamodelFunction(MM2.DR, 'dr', Wave.handlers.ternary_function_to_selected_pages, 'dangling requires')
DS = WaveMetamodelFunction(MM2.DS, 'ds', Wave.handlers.binary_function_to_selected_pages, 'dangling supplies')

F1 = [DR, DS]
mm2 = WaveMetamodel('MM2', F1)

class WaveMetamodelMenu():

    def __init__(self, frame, metamodel = mm2):
        self.frame = frame
        self.metamodel = metamodel
        self.init_menus()
        self.bind_handlers()

    def create_handler(self, frame, wave_function):
        def on(event):
            wave_function.handler(frame, wave_function.function, wave_function.name)
        return on

    def init_menus(self):
        self.frame.mm_sub_menu = wx.Menu()
        self.frame.mm_sub_menu_items = {}
        for wave_function in self.metamodel.functions:
            self.frame.mm_sub_menu_items[wave_function.name] = self.frame.mm_sub_menu.Append(wx.NewId(), wave_function.name, wave_function.long_name)
        self.frame.metamodels_menu.AppendSeparator()
        self.frame.metamodels_menu.AppendMenu(-1, self.metamodel.name, self.frame.mm_sub_menu)  

    def bind_handlers(self):
        for wave_function in self.metamodel.functions:
            self.frame.Bind(wx.EVT_MENU, self.create_handler(self.frame, wave_function), self.frame.mm_sub_menu_items[wave_function.name])

