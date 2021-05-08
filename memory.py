
from utils.constants import (
    BOOLEANO,
    ENTERO,
    FLOTANTE,
    CHAR,
    PROCESO
)

class Memory():

    def __init__(self):
        self.global_space = {
            ENTERO: {
                "min": 1000,
                "max": 2999,
                "current": 1000
            },
            FLOTANTE: {
                "min": 3000,
                "max": 5999,
                "current": 3000
            },
            CHAR: {
                "min": 6000,
                "max": 8999,
                "current": 6000
            },
            BOOLEANO: {
                "min": 9000,
                "max": 11999,
                "current": 9000
            }
        }

        self.local_space = {
            ENTERO: {
                "min": 12000,
                "max": 14999,
                "current": 12000
            },
            FLOTANTE: {
                "min": 13000,
                "max": 15999,
                "current": 13000
            },
            CHAR: {
                "min": 16000,
                "max": 18999,
                "current": 16000
            },
            BOOLEANO: {
                "min": 19000,
                "max": 21999,
                "current": 19000
            }
        }

        self.cte_space = {
            ENTERO: {
                "min": 1000,
                "max": 2999,
                "current": 1000
            },
            FLOTANTE: {
                "min": 3000,
                "max": 5999,
                "current": 3000
            },
            CHAR: {
                "min": 6000,
                "max": 8999,
                "current": 6000
            },
            BOOLEANO: {
                "min": 9000,
                "max": 11999,
                "current": 9000
            }
        }

        self.cte_vars = {}
    
    def reset_local_memory(self):
        for key in self.local_space.keys():
            self.local_space[key]["current"] = self.local_space[key]["min"]


    def set_memory_address(self, var_type, function):
        scope = function["tipo_retorno"]
        if scope == PROCESO:
            return self.set_global_address(var_type)
        return self.set_local_address(var_type)
        
    
    def set_global_address(self, var_type):
        if self.global_space[var_type]["current"] <= self.global_space[var_type]["max"]:
            address = self.global_space[var_type]["current"]
            self.global_space[var_type]["current"] += 1
            return address
        else: 
            raise Exception("Out of memory")
        

    def set_local_address(self, var_type):
        if self.local_space[var_type]["current"] <= self.local_space[var_type]["max"]:
            address = self.local_space[var_type]["current"]
            self.local_space[var_type]["current"] += 1
            return address
        else: 
            raise Exception("Out of memory")