

class TableVariables(): 

    def __init__ (self):
        self.variables = {}

    def insertVariable(self, val):
        variable_declared = self.variables.get(val["key"], None)
        if not variable_declared:
            self.variables[ val["key"] ] = {
                "tipo": val["tipo"],
                "valor": val["value"] if val.get("value", None) else None,
                "direccion": val["direccion"],
                "dimension": val.get("dimension")
            }
            return True
        else: 
            return False

    def get_var(self, var_name):
        # print(var_name)
        # print(self.variables)
        return self.variables.get(var_name)


        