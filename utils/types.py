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

# regresa el tipo de operador
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

# regresa qué tipo de scope tiene la variable
# para eso, revisa el rango de las variables
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


# recibe la direccion de memoria, revisa cada scope para determinar si es det ipo entero, flotante, char u objeto
def get_type_from_address(address):
    if isinstance(address, str):
        address = address.replace('(', '').replace(')', '').replace('dir-', '')
        address = int(address)
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

# revisa qué tipo de constante es la variable
def get_cte_variable(var):
    if re.search(r'([0-9]+)(\.)([0-9]+)', var):
        return FLOTANTE
    elif re.search(r'[0-9]+', var):
        return ENTERO
    elif re.search(r'\".*\"', var):
        return CHAR
    elif re.search(r'(verdadero)|(falso)', var):
        return BOOLEANO
    return None


# revisa si el tipo de variable es un objeto o no
def is_object(var):
    return (var not in [FLOTANTE, ENTERO, CHAR, BOOLEANO])
    
# revisa si la operacion que se quiere hacer da error, sino devolver el tipo resultante
def get_type_operation(op1, op2, operator):
    op = get_operator_type(operator)

    if op:
        return TYPE_MATCHING[op1][op2][op]
    else: 
        raise Exception(f"Operator no mapeado -> {operator}")
