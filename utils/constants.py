PROCESO = "PROCESO"
PRINCIPAL = "PRINCIAPAL"
CTE = "constante"
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
ALL_OPERATIONS = OPER_ARIT_PRIM + OPER_ARIT_SEC + OPER_LOG + OPER_REL
ARIT_PRIM = "AritmeticoPrimario"
ARIT_SEC = "AritmeticoSecundario"
ARIT_LOG = "AritmeticoLogico"
ARIT_REL = "AritmeticoRelacional"

GOTO = "Goto"
GOTO_F = "GotoF"
GOTO_V = "GotoV"
LECTURA = "LECTURA"
ESCRIBE = "ESCRIBE"

GLOBAL_SPACE_ADDRESS = {
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

LOCAL_SPACE_ADDRESS = {
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

CTE_SPACE_ADDRESS = {
    ENTERO: {
        "min": 50,
        "max": 100,
        "current": 50
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