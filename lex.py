from sly import Lexer

class Lex(Lexer):

    tokens = {
        PROGRAMA, ENTERO, FLOTANTE, CHAR, VOID, FUNCTION, LEE, REGRESA, ESCRIBE, MIENTRAS, HACER, DESDE, HASTA, SI, ENTONCES, SINO, , VARIABLES, ID, SEMICOLON, COMMA, LP, RP, LB, RB, LK, RK, ASSIGN, OP_REL, OP_ARIT, OP_LOG, CTE_F, CTE_I, CTE_STRING
    }
        
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*(\[\d+,\d+\])?'

    ID['programa'] = PROGRAMA
    ID['entero'] = ENTERO
    ID['flotante'] = FLOTANTE
    ID['char'] = CHAR
    ID['void'] = VOID
    ID['funcion'] = FUNCTION
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
    LB = r'\['
    RB = r'\]'
    LK = r'\{'
    RK = r'\}'
    ASSIGN = r'\='

    OP_REL = r'(<>|<=|>=|<|>|==|!=)'
    OP_ARIT = r'(\+|-|\*|\/|)'
    OP_LOG = r'(&|\|)'

    CTE_F = r'([0-9]+)(\.)([0-9]+)'
    CTE_I = r'[0-9]+'
    CTE_STRING = r'\".*\"'
    
    
    ignore = '\t'
    ignore_newline = r'\n+'
    
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        raise ValueError('Illegal character')