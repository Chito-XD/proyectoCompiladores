from sly import Parser
from lex import Lex

class Yacc(Parser):
    
    tokens = Lex.tokens

    def __init__(self):
        self.names = {}

    
    ######## PROGRAMA ########
    @_('PROGRAMA ID SEMICOLON PRINCIPAL', 'PROGRAMA ID SEMICOLON DEC_VARS PRINCIPAL', 'PROGRAMA ID SEMICOLON DEC_VARS DEC_FUNC PRINCIPAL')
    def program(self, p):
        return p


    ######## BLOQUE ########
    @_('LK RK', 'LK bloque_aux RK')
    def bloque(self, p):
        return p
    
    @_('estatuto', 'estatuto bloque_aux')
    def bloque_aux(self, p):
        return p

    ######## ESTATUTO ########
    @_('asignacion', 'funcion_void', 'retorno', 'lectura', 'escritura'  'decision', 'repeticion')
    def estatuto(self, p):
        return p
    
    ######## RETORNO ########
    @_('REGRESA LP expresion RP SEMICOLON')
    def retorno(self, p):
        return p
    
    ######## LECTURA ########
    @_('LEE LP lectura_aux RP SEMICOLON')
    def lectura(self, p):
        return p

    @_('ID', 'ID COMMA lectura_aux')
    def lectura_aux(self, p):
        return p

    ####### ESCRITURA ########
    @_('ESCRIBE LP escritura_aux RP SEMICOLON')
    def escritura(self, p):
        return p
    
    @_('expresion', 'CTE_STRING', 'expresion COMMA escritura_aux', 'CTE_STRING COMMA escritura_aux')
    def escritura_aux(self, p):
        return p

    ####### DECISION ########
    @_('SI LP expresion RP bloque SEMICOLON', 'SI LP expresion RP bloque SINO bloque')
    def decision(self, p):
        return p
    
    ####### REPETICION ######## 
    # revisar el desde
    @_('MIENTRAS LP expresion RP HACER bloque', 'DESDE')
    def repeticion(self, p):
        return p

    ####### EXPRESION ########
    @_('exp', 'exp OP_REL exp')
    def expresion(self, p):
        return p

    ####### EXP ########
    @_('termino', 'termino OP_ARIT exp')
    def exp(self, p):
        return p

    ####### TERMINO ########
    @_('factor', 'factor OP_ARIT termino')
    def termino(self, p):
        return p


    ######## FACTOR ########
    @_('LP expresion RP', 'var_cte', 'OP_ARIT var_cte')
    def factor(self, p):
        return p


    ######## VAR_CTE ########
    @_('ID', 'CTE_I', 'CTE_F')
    def var_cte(self, p):
        return p


    ######## TIPO ########
    @_('ENTERO', 'FLOTANTE', 'CHAR', 'VOID', 'ID')
    def tipo(self, p):
        return p