import re
from utils.constants import (
    TYPE_MATCHING, 
    OPER_ARIT_PRIM,
    ARIT_PRIM,
    OPER_ARIT_SEC,
    ARIT_SEC,
    OPER_LOG,
    ARIT_LOG,
    OPER_REL,
    ARIT_REL,
    EQUAL,
    ASSIGN,
    FLOTANTE,
    ENTERO,
    CHAR,
    ID,
    BOOLEANO,
    GLOBAL_SPACE_ADDRESS,
    LOCAL_SPACE_ADDRESS,
    CTE_SPACE_ADDRESS
)

def get_operator_type(operator):
    if operator in OPER_ARIT_PRIM:
        return ARIT_PRIM
    elif operator in OPER_ARIT_SEC:
        return ARIT_SEC
    elif operator in OPER_LOG:
        return ARIT_LOG
    elif operator in OPER_REL:
        return ARIT_REL
    elif operator == ASSIGN:
        return ASSIGN
    else:
        return None
    
def get_scope_from_address(address):
    for key in GLOBAL_SPACE_ADDRESS.keys():
        if address >= GLOBAL_SPACE_ADDRESS[key]["min"] and address <= GLOBAL_SPACE_ADDRESS[key]["max"]:
            return "GLOBAL"
        
    for key in LOCAL_SPACE_ADDRESS.keys():
        if address >= LOCAL_SPACE_ADDRESS[key]["min"] and address <= LOCAL_SPACE_ADDRESS[key]["max"]:
            return "LOCAL"
        
    for key in CTE_SPACE_ADDRESS.keys():
        if address >= CTE_SPACE_ADDRESS[key]["min"] and address <= CTE_SPACE_ADDRESS[key]["max"]:
            return "CTE"
    
    raise Exception("-> No memory range found")

def get_type_from_address(address):
    for key in GLOBAL_SPACE_ADDRESS.keys():
        if address >= GLOBAL_SPACE_ADDRESS[key]["min"] and address <= GLOBAL_SPACE_ADDRESS[key]["max"]:
            return key
        
    for key in LOCAL_SPACE_ADDRESS.keys():
        if address >= LOCAL_SPACE_ADDRESS[key]["min"] and address <= LOCAL_SPACE_ADDRESS[key]["max"]:
            return key
        
    for key in CTE_SPACE_ADDRESS.keys():
        if address >= CTE_SPACE_ADDRESS[key]["min"] and address <= CTE_SPACE_ADDRESS[key]["max"]:
            return key
    
    raise Exception("-> No memory range found")

def get_cte_variable(var):
    if re.search(r'([0-9]+)(\.)([0-9]+)', var):
        return FLOTANTE
    elif re.search(r'[0-9]+', var):
        return ENTERO
    elif re.search(r'\".*\"', var):
        return CHAR
    elif re.search(r'(verdadero)|(falso)', var):
        return BOOLEANO
    # elif re.search(r'[a-zA-Z_][a-zA-Z_0-9]*', var):
    #     return ID
    return None
    

def get_type_operation(op1, op2, operator):
    op = get_operator_type(operator)

    if op:
        return TYPE_MATCHING[op1][op2][op]
    else: 
        raise Exception(f"Operator no mapeado -> {operator}")
