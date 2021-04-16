

class TableVariables(): 

    def __init__ (self):
        self.variables = None

    def insertVariable(self, val):
        if not self.variables:
            self.variables = {}

        variable_declared = self.variables.get(val["key"], None)
        if not variable_declared:
            self.variables[ val["key"] ] = {
                tipo: val["tipo"]
                valor: val["value"]
                # demás parámetros ...
            }
        else: 
            raise Exception("La variable ya existe")

    def updateVariable(self, var):
        if var["key"] in self.variables.keys():
            self.variables[ var["key"] ] = var["value"]
        else:
            raise Exception("No existe la variable")
        