from sly import Lexer

class Lex(Lexer):

    tokens = {
        PROGRAMA, CLASE, HEREDA, ATRIBUTOS, METODOS, PRINCIPAL, VARIABLES, ENTERO, FLOTANTE, CHAR, VOID, BOOLEAN,  FUNCION, LEE, REGRESA, ESCRIBE, MIENTRAS, HACER, DESDE, HASTA, SI, ENTONCES, SINO, ID, SEMICOLON, COMMA, LP, RP, LK, RK, ASSIGN, OP_REL, OP_ARIT_SEC, OP_ARIT_PRIM, OP_LOG, CTE_F, CTE_I, CTE_STRING, DOTS, DOT, LC, RC
    }

    ignore = ' \t'
    # ignore_comment = r'\#.*'
    ignore_newline = r' \n+'
        
    ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

    ID['variables'] = VARIABLES
    ID['Clase'] = CLASE
    ID['hereda'] = HEREDA
    ID['atributos'] = ATRIBUTOS
    ID['metodos'] = METODOS
    ID['programa'] = PROGRAMA
    ID['principal'] = PRINCIPAL
    ID['entero'] = ENTERO
    ID['flotante'] = FLOTANTE
    ID['char'] = CHAR
    ID['void'] = VOID
    ID['booleano'] = BOOLEAN
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
    
    OP_REL = r'(<>|<=|>=|<|>|(==)|!=)'
    SEMICOLON = r'\;'
    COMMA = r'\,'
    LP = r'\('
    RP = r'\)'
    LC = r'\['
    RC = r'\]'
    LK = r'\{'
    RK = r'\}'
    ASSIGN = r'\='

    
    OP_ARIT_SEC = r'(\+|-)'
    OP_ARIT_PRIM = r'(\*|\/)'
    OP_LOG = r'(&|\|)'

    CTE_F = r'([0-9]+)(\.)([0-9]+)'
    CTE_I = r'[0-9]+'
    CTE_STRING = r'\".*\"'
    DOTS = r'\:'
    DOT = r'\.'
    
    
    # @_(r'\n+')
    # def ignore_newline(self, t):
    #     self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1
        raise ValueError('Illegal character')