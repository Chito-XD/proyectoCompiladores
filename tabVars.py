

class TableVariables(): 

    def __init__ (self):
        self.variables = {}

    def insertVariable(self, val):
        variable_declared = self.variables.get(val["key"], None)
        if not variable_declared:
            self.variables[ val["key"] ] = {
                "tipo": val["tipo"],
                "valor": val["value"] if val.get("value", None) else None,
                "direccion": None
            }
            return True
        else: 
            return False

    def updateVariable(self, var):
        if var["key"] in self.variables.keys():
            self.variables[ var["key"] ] = var["value"]
            return True
        else:
            return False
        