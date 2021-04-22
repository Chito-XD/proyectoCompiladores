

from constants import (
    TYPE_MATCHING, 
    OPER_ARIT_PRIM,
    ARIT_PRIM,
    OPER_ARIT_SEC,
    ARIT_SEC,
    OPER_LOG,
    ARIT_LOG,
    OPER_REL,
    ARIT_REL,
    EQUAL
)

def get_operator_type(operator):
    if operator in OPER_ARIT_PRIM:
        return ARIT_PRIM
    if operator in OPER_ARIT_SEC:
        return ARIT_SEC
    if operator in OPER_LOG:
        return ARIT_LOG
    if operator in OPER_REL:
        return ARIT_REL

def get_type_from_operator(op1, op2, operator):
    return TYPE_MATCHING[op1][op2][get_operator_type(operator)]

def get_value_from_operator(op1, op2, operator):
    # Igualdad
    if operator is EQUAL:
        return op1

    # Operador lógico
    if operator in OPER_LOG:
        if operator is '&':
            return (op1 and op2)
        else:
            return (op1 or op2)
    

    # GOTO

    # Caso base (Operadores aritméticos, relacionales)
    return eval( op1 + operator + op2)