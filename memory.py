
from utils.constants import (
    GLOBAL_SPACE_ADDRESS,
    LOCAL_SPACE_ADDRESS,
    CTE_SPACE_ADDRESS,
    PROCESO
)

class Memory():

    def __init__(self):
        self.cte_vars = {}
    
    def reset_local_memory(self):
        for key in LOCAL_SPACE_ADDRESS.keys():
            LOCAL_SPACE_ADDRESS[key]["current"] = LOCAL_SPACE_ADDRESS[key]["min"]


    def set_memory_address(self, var_type, scope, var_size=1):
        if scope == PROCESO:
            return self.set_global_address(var_type, var_size)
        return self.set_local_address(var_type, var_size)
    
    def get_cte_address(self, var_type, var):
        if self.cte_vars.get(var):
            return self.cte_vars.get(var)
        
        cte_address = self.set_cte_address(var_type)
        self.cte_vars[var] = cte_address
        return cte_address


    def set_cte_address(self, var_type):
        if CTE_SPACE_ADDRESS[var_type]["current"] <= CTE_SPACE_ADDRESS[var_type]["max"]:
            address = CTE_SPACE_ADDRESS[var_type]["current"]
            CTE_SPACE_ADDRESS[var_type]["current"] += 1
            return address
        else: 
            raise Exception("Out of memory")

    def set_global_address(self, var_type, var_size):
        if GLOBAL_SPACE_ADDRESS[var_type]["current"] <= GLOBAL_SPACE_ADDRESS[var_type]["max"]:
            address = GLOBAL_SPACE_ADDRESS[var_type]["current"]
            GLOBAL_SPACE_ADDRESS[var_type]["current"] += var_size
            return address
        else: 
            raise Exception("Out of memory")
        

    def set_local_address(self, var_type, var_size):
        if LOCAL_SPACE_ADDRESS[var_type]["current"] <= LOCAL_SPACE_ADDRESS[var_type]["max"]:
            address = LOCAL_SPACE_ADDRESS[var_type]["current"]
            LOCAL_SPACE_ADDRESS[var_type]["current"] += var_size
            return address
        else: 
            raise Exception("Out of memory")