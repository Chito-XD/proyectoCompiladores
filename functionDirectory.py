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
        self.proceso_main = None
    
    # Funcion para crear una funcion
    def createFunction(self, key, params):
        if key not in self.directory.keys():
            self.directory[key] = {
                "tipo_retorno": params["tipo"],
                "directorio_variables": TableVariables()
            }
            if params["tipo"] == PROCESO:
                self.proceso_main = self.directory[key]
        else :
            raise Exception(f"--> La función {key} ya existe")
    
    ##Funcion para agregar las variables locales de las funciones
    def addLocalVariable(self, key, var):
        if key in self.directory.keys():
            is_inserted = self.directory[key]["directorio_variables"].insertVariable(var)
            if not is_inserted:
                raise Exception(f"--> La variable {var['key']} ya existe en la funcion {key}")
        else:
            raise Exception(f"--> No existe la funcion {key}")   
    
    # Funcion para actualizar el valor de una variable de un método
    def updateVariable(self, key, var):
        if key in self.directory.keys():
            is_updated = self.directory[key]["directorio_variables"].updateVariable(var)
            if not is_updated:
                raise Exception(f"--> No se puede actualizar una variable que no existe en la funcion {key} --> {var['key']}")
        else:
            raise Exception(f"--> No existe la funcion {key}")

    def get_variable(self, key, var):
        if key in self.directory.keys():
            variables = self.directory[key]["directorio_variables"].variables
            if var in variables.keys():
                return variables[var]
            else:
                variables = self.proceso_main["directorio_variables"].variables
                if var in variables.keys():
                    return variables[var]
                else:
                    raise(f"No existe la variable {var} en la funcion {key}")
        else:
            raise Exception(f"--> No existe la funcion {key}")
    
            


