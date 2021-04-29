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
    BOOLEANO
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

def get_type_variable(var):
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

def evaluate_operation(op1, op2, operator):
    # Operador lógico
    if operator in OPER_LOG:
        if operator == '&':
            return (op1 and op2)
        else:
            return (op1 or op2)
    
    # Caso base (Operadores aritméticos, relacionales)
    return eval( op1 + operator + op2)