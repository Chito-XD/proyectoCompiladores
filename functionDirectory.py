from tabVars import TableVariables
from constansts import PROCESO

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
    

    def createFunction(self, key, params):
        unused_key = self.directory.get(key, None)
        if unused_key: 
            self.directory[key] = {
                tipo_retorno: params.tipo,
                #  Valores extra del directorio de funciones
                directorio_variables: TableVariables(params.values, self.proceso_main)
            }
            if params.tipo == PROCESO:
                self.proceso_main = self.directory[key]
        else :
            raise Exception("La función ya existe")
    
    ##Funcion para agregar las variables locales de las funciones
    def addLocalVariables(self, key, vars){
        if key in directory.keys():
            self.directory[key].directorio_variables.insertVariables(vars)
        else:
            raise Exception("No existe esa funcion")   
    }

    #def updateVariables(self, keyFunc, var){
    #    if keyFunc in directory.keys():
    #        self.directory[key].directorio_variables.updateVariable(var)
    #    else:
    #        raise Exception("No existe esa funcion") 
    #}
            


