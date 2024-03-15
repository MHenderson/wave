class Function():

    def __init__(self, function, fix = False, symbol = False, name = False):
        self.function = function
        self.fix = fix
        self.symbol = symbol
        self.name = name

    def __call__(self, *vargs):
        return self.function(*vargs)

    def get_function(self):
        return self.function

    def nargs(self):
        return self.function.func_code.co_argcount
         
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


