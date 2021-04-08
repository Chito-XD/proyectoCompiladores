from sly import Lexer

class Lex(Lexer):

    tokens = {
        PROGRAMA, PRINCIPAL, VARIABLES, ENTERO, FLOTANTE, CHAR, VOID, FUNCION, LEE, REGRESA, ESCRIBE, MIENTRAS, HACER, DESDE, HASTA, SI, ENTONCES, SINO, VARIABLES, ID, SEMICOLON, COMMA, LP, RP, LK, RK, ASSIGN, OP_REL, OP_ARIT_SEC, OP_ARIT_PRIM, OP_LOG, CTE_F, CTE_I, CTE_STRING, DOTS
    }
        
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*(\[\d+,\d+\])?'

    ID['programa'] = PROGRAMA
    ID['principal'] = PRINCIPAL
    ID['variables'] = VARIABLES
    ID['entero'] = ENTERO
    ID['flotante'] = FLOTANTE
    ID['char'] = CHAR
    ID['void'] = VOID
    ID['funcion'] = FUNCION
    ID['lee'] = LEE
    ID['regresa'] = REGRESA
    ID['escribe'] = ESCRIBE
    ID['mientras'] = MIENTRAS
    ID['hacer'] = HACER
    ID['desde'] = DESDE
    ID['hasta'] = HASTA
    ID['si'] = SI
    ID['entonces'] = ENTONCES
    ID['sino'] = SINO
    ID['variables'] = VARIABLES
    
    SEMICOLON = r'\;'
    COMMA = r'\,'
    LP = r'\('
    RP = r'\)'
    LK = r'\{'
    RK = r'\}'
    ASSIGN = r'\='

    OP_REL = r'(<>|<=|>=|<|>|==|!=)'
    OP_ARIT_SEC = r'(\+|-)'
    OP_ARIT_PRIM = r'(\*|\/)'
    OP_LOG = r'(&|\|)'

    CTE_F = r'([0-9]+)(\.)([0-9]+)'
    CTE_I = r'[0-9]+'
    CTE_STRING = r'\".*\"'
    DOTS = r'\:'
    
    
    ignore = ' \t'
    # ignore_newline = r' \n+'
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        raise ValueError('Illegal character')