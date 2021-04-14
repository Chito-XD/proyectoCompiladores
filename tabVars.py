

class TableVariables(): 

    def __init__ (self, values, proceso_main):
        self.variables = {}
        self.global_variables = None
        if proceso_main is not None: 
            self.global_variables = proceso_main.directorio_variables.variables
        self.insertVariables(values)
    

    def insertVariables(self, values):
        for val in values:
            variable_declared = self.variables.get(val.key, None)
            if not variable_declared:
                self.variables[val.key] = {
                    tipo: val.tipo
                    # demás parámetros ...
                }
            else: 
                raise Exception("La variable ya existe")