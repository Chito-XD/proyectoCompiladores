

class TableVariables(): 

    def __init__ (self):
        self.variables = {}

    def insertVariable(self, val):
        variable_declared = self.variables.get(val["key"], None)
        if not variable_declared:
            self.variables[ val["key"] ] = {
                "tipo": val["tipo"],
                "valor": val["value"] if val.get("value", None) else None,
                "direccion": val["direccion"]
            }
            return True
        else: 
            return False
        
    def get_type(self, var_name):
        return self.variables[var_name]["tipo"]
        
    def get_address(self, var_name):
        print("GET ADDRES")
        print(self.variables)
        print(var_name)
        return self.variables[var_name]["direccion"]

        