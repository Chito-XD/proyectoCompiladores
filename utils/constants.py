PROCESO = "PROCESO"
PRINCIPAL = "PRINCIAPAL"
MAIN = "Main"
CTE = "constante"
ENTERO = "entero"
FLOTANTE = "flotante"
VOID = "void"
CHAR = "char"
ID = "id"
OBJECT = "objeto"
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
GOSUB = "GOSUB"
PARAM = "PARAM"
ERA = "ERA"
REGRESA = "REGRESA"
VERIFICA = "VERIFICA"
END_FUNCTION = "END_FUNCTION"
LECTURA = "LECTURA"
ESCRIBE = "ESCRIBE"

GLOBAL_SPACE_ADDRESS = {
    ENTERO: {
        "min": 5000,
        "max": 5999,
        "current": 5000
    },
    FLOTANTE: {
        "min": 6000,
        "max": 6999,
        "current": 6000
    },
    CHAR: {
        "min": 7000,
        "max": 7999,
        "current": 7000
    },
    BOOLEANO: {
        "min": 8000,
        "max": 8999,
        "current": 8000
    },
    OBJECT: {
        "min": 9000,
        "max": 9999,
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
    },
    OBJECT: {
        "min": 22000,
        "max": 23999,
        "current": 22000
    }
}

CTE_SPACE_ADDRESS = {
    ENTERO: {
        "min": 25000,
        "max": 27999,
        "current": 25000
    },
    FLOTANTE: {
        "min": 28000,
        "max": 30999,
        "current": 28000
    },
    CHAR: {
        "min": 31000,
        "max": 33999,
        "current": 31000
    },
    BOOLEANO: {
        "min": 34000,
        "max": 36999,
        "current": 34000
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