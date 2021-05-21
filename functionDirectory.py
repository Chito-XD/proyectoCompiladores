from utils.constants import PROCESO
from tabVars import TableVariables

class FunctionDirectory():
    
# directorio_funciones = {
#     pelos_quitos: {
#         tipo_retorno: "NP",
#         ...,
#         directorio_variables: TableVariables()
#     },

#     modulo1: {
#         tipo_retorno: "void",
#         ...,
#         directorio_variables: TableVariables()
#     },
#     ...
# }

    def __init__(self):
        self.directory = {}
    
    def createClass(self, class_name):
        if class_name not in self.directory.keys():
            self.directory[class_name] = {}
        else:
            raise Exception(f"--> La clase {class_name} ya existe")


    # Funcion para crear una funcion
    def createFunction(self, class_name, function_name, params):
        if class_name in self.directory.keys():
            if function_name not in self.directory[class_name].keys():
                if params["tipo"] == PROCESO:
                    self.directory[class_name]["proceso_global"] = function_name
                self.directory[class_name][function_name] = {
                    "tipo_retorno": params["tipo"],
                    "directorio_variables": TableVariables(),
                    "inicio": params["inicio"],
                    "parametros": params.get("parametros") if params.get("parametros") else []
                }
            else :
                raise Exception(f"--> La función {function_name} ya existe en la clase {class_name}")
        else:
            raise Exception(f"--> La clase {class_name} no existe")
    
    ##Funcion para agregar las variables locales de las funciones
    def addLocalVariable(self, class_name, function_name, var):
        if class_name in self.directory.keys():
            if function_name in self.directory[class_name].keys():
                is_inserted = self.directory[class_name][function_name]["directorio_variables"].insertVariable(var)
                if not is_inserted:
                    raise Exception(f"--> La variable {var['key']} ya existe en la funcion {function_name} de la clase {class_name}")
            else:
                raise Exception(f"--> No existe la funcion {function_name} en la clase {class_name}")   
        else:
            raise Exception(f"--> La clase {class_name} no existe")
    
    # Funcion para agregar parametros a las funciones
    def addParam(self, class_name, function_name, var):
        self.addLocalVariable(class_name, function_name, var)
        self.directory[class_name][function_name]["parametros"].append(var["tipo"])
    
    # Funcion para actualizar el valor de una variable de un método
    def updateVariable(self, class_name, function_name, var):
        if class_name in self.directory.keys():
            if function_name in self.directory[class_name].keys():
                is_updated = self.directory[class_name][function_name]["directorio_variables"].updateVariable(var)
                if not is_updated:
                    raise Exception(f"--> No se puede actualizar una variable que no existe en la funcion {function_name} de la clase {class_name} --> {var['key']}")
            else:
                raise Exception(f"--> No existe la funcion {function_name} en la clase {class_name}")
        else:
            raise Exception(f"--> La clase {class_name} no existe")

    # funcion para obtener la variable de un metodo - sino lo encuentra lo busca en el global de la clase
    def get_variable(self, class_name, function_name, var):
        if class_name in self.directory.keys():
            if function_name in self.directory[class_name].keys():
                variables = self.directory[class_name][function_name]["directorio_variables"].variables
                if var in variables.keys():
                    return variables[var]
                else:
                    global_class_function = self.directory[class_name]["proceso_global"]
                    variables = self.directory[class_name][global_class_function]["directorio_variables"].variables
                    if var in variables.keys():
                        return variables[var]
                    else:
                        raise Exception(f"No existe la variable {var} en la funcion {function_name} de la clase {class_name}")
            else:
                raise Exception(f"--> No existe la funcion {function_name} en la clase {class_name}")
        else:
            raise Exception(f"--> La clase {class_name} no existe")
    
    
    # regresa el tipo de retorno de la funcion
    def get_tipo_retorno(self, class_name, function_name):
        return self.directory[class_name][function_name].get("tipo_retorno")
    

    def get_dir_variables(self, class_name, function_name):
        return self.directory[class_name][function_name]["directorio_variables"].variables
    
    # imprime el directorio de funciones
    def print_directory(self):
        for class_name in self.directory.keys():
            print('=== CLASS --> ', class_name)
            for function in self.directory[class_name].keys():
                if function == "proceso_global":
                    print('proceso global ---> ', self.directory[class_name][function])
                else:
                    print('funcion ---> ', function)
                    print(self.directory[class_name][function])
                    var = self.directory[class_name][function]["directorio_variables"].variables
                    print(var)
                print("")
            print("")
    
            


