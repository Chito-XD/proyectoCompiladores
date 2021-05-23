
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
    
    def reset_local_memory(self):
        for key in LOCAL_SPACE_ADDRESS.keys():
            LOCAL_SPACE_ADDRESS[key]["current"] = LOCAL_SPACE_ADDRESS[key]["min"]
        
    def reset_global_memory(self):
        for key in GLOBAL_SPACE_ADDRESS.keys():
            GLOBAL_SPACE_ADDRESS[key]["current"] = GLOBAL_SPACE_ADDRESS[key]["min"]


    def set_memory_address(self, var_type, scope):
        if scope == PROCESO:
            return self.set_global_address(var_type)
        return self.set_local_address(var_type)
    
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

    def set_global_address(self, var_type):
        if is_object(var_type):
            var_type = OBJECT
        if GLOBAL_SPACE_ADDRESS[var_type]["current"] <= GLOBAL_SPACE_ADDRESS[var_type]["max"]:
            address = GLOBAL_SPACE_ADDRESS[var_type]["current"]
            GLOBAL_SPACE_ADDRESS[var_type]["current"] += 1
            return address
        else: 
            raise Exception("Out of memory")
        

    def set_local_address(self, var_type):
        if is_object(var_type):
            var_type = OBJECT
        if LOCAL_SPACE_ADDRESS[var_type]["current"] <= LOCAL_SPACE_ADDRESS[var_type]["max"]:
            address = LOCAL_SPACE_ADDRESS[var_type]["current"]
            LOCAL_SPACE_ADDRESS[var_type]["current"] += 1
            return address
        else: 
            raise Exception("Out of memory")