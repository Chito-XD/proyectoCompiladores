

class TableVariables(): 

    def __init__ (self, values):
        self.variables = {}
        self.insertVariables(values)
    

    def insertVariables(self, values):
        for val in values:
            variable_declared = self.variables.get(val.key, None)
            if not variable_declared:
                self.variables[val.key] = {
                    tipo: val.tipo
                    valor: None
                    # demás parámetros ...
                }
            else: 
                raise Exception("La variable ya existe")

    def updateVariable(self, var):
        if var.key in self.variables.keys():
            self.variables[var.key] = var.valor
        else:
            raise Exception("No existe la variable")
        