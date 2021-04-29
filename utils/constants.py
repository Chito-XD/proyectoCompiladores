PROCESO = "N/P"
PRINCIPAL = "PRINCIAPAL"
ENTERO = "entero"
FLOTANTE = "flotante"
VOID = "void"
CHAR = "char"
ID = "id"
BOOLEANO = "booleano"
ERROR = "error"
EQUAL = "=="
ASSIGN = "="
OPER_ARIT_PRIM = ['*', '/']
OPER_ARIT_SEC = ['+', '-']
OPER_LOG = ['&', '|']
OPER_REL = ['<>', '<', '>', '<=', '>=', '==', '!=']
ARIT_PRIM = "AritmeticoPrimario"
ARIT_SEC = "AritmeticoSecundario"
ARIT_LOG = "AritmeticoLogico"
ARIT_REL = "AritmeticoRelacional"

TYPE_MATCHING = {
    ENTERO: {
        ENTERO: {
            ARIT_PRIM : ENTERO,
            ARIT_SEC : ENTERO,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO,
            ASSIGN : ENTERO
        },
        FLOTANTE: {
            ARIT_PRIM : FLOTANTE,
            ARIT_SEC : FLOTANTE,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO,
            ASSIGN : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : BOOLEANO,
            ARIT_REL : ERROR,
            ASSIGN: ERROR,
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        }
    },
    FLOTANTE: {
        ENTERO: {
            ARIT_PRIM : FLOTANTE,
            ARIT_SEC : FLOTANTE,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO,
            ASSIGN : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : FLOTANTE,
            ARIT_SEC : FLOTANTE,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO,
            ASSIGN : FLOTANTE
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        }
    },
    VOID: {
        ENTERO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR, 
            ASSIGN : VOID
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        }
    },
    BOOLEANO: {
        ENTERO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : BOOLEANO,
            ARIT_REL : BOOLEANO,
            ASSIGN : BOOLEANO
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        }
    },
    CHAR: {
        ENTERO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        FLOTANTE: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        VOID: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : ERROR,
            ARIT_REL : ERROR,
            ASSIGN : ERROR
        },
        BOOLEANO: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : ERROR,
            ARIT_LOG : BOOLEANO,
            ARIT_REL : BOOLEANO,
            ASSIGN : ERROR
        },
        CHAR: {
            ARIT_PRIM : ERROR,
            ARIT_SEC : CHAR,
            ARIT_LOG : ERROR,
            ARIT_REL : BOOLEANO,
            ASSIGN : CHAR
        }
    }
}