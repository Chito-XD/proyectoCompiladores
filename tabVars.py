

class TableVariables(): 

    def __init__ (self):
        self.variables = {}

    # Metodo para agregar una variable y sus atributos al diccionario
    def insertVariable(self, val: dict) -> bool:
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

    # Metodo para obtener los atributos de la variable
    def get_var(self, var_name: str) -> dict:
        return self.variables.get(var_name)


        