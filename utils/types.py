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
    ASSIGN
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