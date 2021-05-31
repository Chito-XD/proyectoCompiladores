from utils.types import is_object
from utils.constants import (
    GLOBAL_SPACE_ADDRESS,
    LOCAL_SPACE_ADDRESS,
    CTE_SPACE_ADDRESS,
    PROCESO,
    OBJECT
)

class Memory():

    def __init__(self):
        self.cte_vars = {}
    
    # metodo para resetear la memoria local 
    # se resetea cada vez que se crea un nuevo método
    def reset_local_memory(self) -> None:
        for key in LOCAL_SPACE_ADDRESS.keys():
            LOCAL_SPACE_ADDRESS[key]["current"] = LOCAL_SPACE_ADDRESS[key]["min"]
    
    # metodo para resetear la memoria global 
    # se resetea cada vez que se crea una nueva clase
    def reset_global_memory(self) -> None:
        for key in GLOBAL_SPACE_ADDRESS.keys():
            GLOBAL_SPACE_ADDRESS[key]["current"] = GLOBAL_SPACE_ADDRESS[key]["min"]

    # asingar una memoria temporal a la variable recibida.
    # Dependiendo de la dimension de la variable, son los espacios que utiliza
    # Dependiendo si el scope es global o local, es la dirección que utiliza
    def set_memory_address(self, var_type: str, scope: str, var_size=1) -> int:
        if scope == PROCESO:
            return self.set_global_address(var_type, var_size)
        return self.set_local_address(var_type, var_size)
    
    # regresa la dirección de memoria de la constante dada
    def get_cte_address(self, var_type: str, var: str) -> int:
        if self.cte_vars.get(var):
            return self.cte_vars.get(var)
        
        # si no encuentra la direccion, crea una una nueva dirección para la constante
        cte_address = self.set_cte_address(var_type)
        self.cte_vars[var] = cte_address
        return cte_address

    # Asigna una direccion de memoria a la constante recibida.

    def set_cte_address(self, var_type: str) -> int :
        if CTE_SPACE_ADDRESS[var_type]["current"] <= CTE_SPACE_ADDRESS[var_type]["max"]:
            address = CTE_SPACE_ADDRESS[var_type]["current"]
            # aumenta el valor actual dependiendo del tamaño y dimension de la variable
            CTE_SPACE_ADDRESS[var_type]["current"] += 1
            return address
        else: 
            # si se excede la cantidad de memoria, lanza error
            raise Exception("Out of memory")

    # Asigna una direccion de memoria a la variable global
    def set_global_address(self, var_type: str, var_size: int)-> int:
        if is_object(var_type):
            var_type = OBJECT
        if GLOBAL_SPACE_ADDRESS[var_type]["current"] <= GLOBAL_SPACE_ADDRESS[var_type]["max"]:
            address = GLOBAL_SPACE_ADDRESS[var_type]["current"]
            # aumenta el valor actual dependiendo del tamaño y dimension de la variable
            GLOBAL_SPACE_ADDRESS[var_type]["current"] += var_size
            return address
        else: 
            # si se excede la cantidad de memoria, lanza error
            raise Exception("Out of memory")
        
    # Asigna una direccion de memoria a la variable local
    def set_local_address(self, var_type: str, var_size: int) -> int:
        if is_object(var_type):
            var_type = OBJECT
        if LOCAL_SPACE_ADDRESS[var_type]["current"] <= LOCAL_SPACE_ADDRESS[var_type]["max"]:
            address = LOCAL_SPACE_ADDRESS[var_type]["current"]
            # aumenta el valor actual dependiendo del tamaño y dimension de la variable
            LOCAL_SPACE_ADDRESS[var_type]["current"] += var_size
            return address
        else: 
            # si se excede la cantidad de memoria, lanza error
            raise Exception("Out of memory")