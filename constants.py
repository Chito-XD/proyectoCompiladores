PROCESO = "N/P"
PRINCIPAL = "PRINCIAPAL"
ENTERO = "entero"
FLOTANTE = "flotante"
VOID = "void"
CHAR = "char"
BOOLEANO = "booleano"
ERROR = "error"
OPER_ARIT_PRIM = ['*', '/']
OPER_ARIT_SEC = ['+', '-']
OPER_LOG = ['&', '|']
OPER_REL = ['<>', '<', '>', '<=', '>=', '==', '!=']
ARIT_PRIM = "AritmeticoPrimario"
ARIT_SEC = "AritmeticoSecundario"
ARIT_LOG = "AritmeticoLogico"
ARIT_REL = "AritmeticoRelacional"

def getOperatorType(operator):
    if operator in OPER_ARIT_PRIM:
        return ARIT_PRIM
    if operator in OPER_ARIT_SEC:
        return ARIT_SEC
    if operator in OPER_LOG:
        return ARIT_LOG
    if operator in OPER_REL:
        return ARIT_REL

TYPE_MATCHING = {
    ENTERO: {
        ENTERO: {
            ARIT_PRIM : ENTERO,
            ARIT_SEC : ENTERO,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO
        },
        FLOTANTE: {
            ARIT_PRIM : FLOTANTE,
            ARIT_SEC : FLOTANTE,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : BOOLEANO,
            ARIT_REL : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        }
    },
    FLOTANTE: {
        ENTERO: {
            ARIT_PRIM : FLOTANTE,
            ARIT_SEC : FLOTANTE,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO
        },
        FLOTANTE: {
            ARIT_PRIM : FLOTANTE,
            ARIT_SEC : FLOTANTE,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        }
    },
    VOID: {
        ENTERO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        }
    },
    BOOLEANO: {
        ENTERO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : BOOLEANO,
            ARIT_REL : BOOLEANO
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
        }
    },
    CHAR: {
        ENTERO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : BOOLEANO,
            ARIT_REL : BOOLEANO
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : CHAR,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO
        }
    }
}