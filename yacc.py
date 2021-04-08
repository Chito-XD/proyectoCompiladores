from sly import Parser
from lex import Lex

class Yacc(Parser):
    
    tokens = Lex.tokens

    def __init__(self):
        self.names = {}

    
    ######## PROGRAMA ########
    @_('PROGRAMA ID SEMICOLON principal', 'PROGRAMA ID SEMICOLON dec_vars principal', 'PROGRAMA ID SEMICOLON dec_vars dec_func principal', 'PROGRAMA ID SEMICOLON dec_func PRINCIPAL')
    def program(self, p):
        return p
    
    ######## PRINCIPAL ########
    @_('PRINCIPAL LP RP bloque')
    def principal(self, p):
        return p

    ######## DEC_VARS ########
    @_('VARIABLES dec_vars_aux DOTS tipo SEMICOLON dec_vars', 'VARIABLES dec_vars_aux DOTS tipo SEMICOLON')
    def dec_vars(self, p):
        return p
    
    @_('ID COMMA dec_vars_aux', 'ID')
    def dec_vars_aux(self, p):
        return p

    ######## PARAMETROS ########
    @_('ID COMMA tipo COMMA parametros', 'ID COMMA tipo')
    def parametros(self, p):
        return p
    
    ######## DEC_FUNC ########
    @_('tipo FUNCION ID LP parametros RP SEMICOLON dec_vars bloque', 'tipo FUNCION ID LP parametros RP SEMICOLON bloque','tipo FUNCION ID LP RP SEMICOLON dec_vars bloque','tipo FUNCION ID LP RP SEMICOLON bloque')
    def dec_func(self, p):
        return p

    ######## BLOQUE ########
    @_('LK RK', 'LK bloque_aux RK')
    def bloque(self, p):
        return p
    
    @_('estatuto bloque_aux', 'estatuto')
    def bloque_aux(self, p):
        return p

    ######## ESTATUTO ########
    @_('asignacion', 'funcion', 'retorno', 'lectura', 'escritura', 'decision', 'repeticion')
    def estatuto(self, p):
        return p

    ######## ASIGNACION ########
    @_('ID ASSIGN expresion SEMICOLON', 'ID ASSIGN funcion asignacion_aux', 'ID ASSIGN funcion')
    def asignacion(self, p):
        return p
    
    @_('expresion asignacion_aux', 'expresion')
    def asignacion_aux(self, p):
        return p
    
    ######## LLAMADA FUNCION ########
    @_('ID LP funcion_aux RP SEMICOLON')
    def funcion(self, p):
        return p
    
    @_('expresion COMMA funcion_aux', 'expresion')
    def funcion_aux(self, p):
        return p

    ######## RETORNO ########
    @_('REGRESA LP expresion RP SEMICOLON')
    def retorno(self, p):
        return p
    
    ####### ESCRITURA ########
    @_('ESCRIBE LP escritura_aux RP SEMICOLON')
    def escritura(self, p):
        return p
    
    @_('expresion COMMA escritura_aux', 'CTE_STRING COMMA escritura_aux', 'expresion', 'CTE_STRING',)
    def escritura_aux(self, p):
        return p
    
    ######## LECTURA ########
    @_('LEE LP lectura_aux RP SEMICOLON')
    def lectura(self, p):
        return p

    @_('ID COMMA lectura_aux', 'ID')
    def lectura_aux(self, p):
        return p

    ####### DECISION ########
    @_('SI LP expresion RP bloque SINO bloque', 'SI LP expresion RP bloque SEMICOLON')
    def decision(self, p):
        return p
    
    ####### REPETICION ######## 
    # revisar el desde
    @_('MIENTRAS LP expresion RP HACER bloque', 'DESDE ID ASSIGN expresion HASTA expresion HACER bloque')
    def repeticion(self, p):
        return p
    
    ######## TIPO ########
    @_('ENTERO', 'FLOTANTE', 'CHAR', 'VOID')
    def tipo(self, p):
        return p

    ####### EXPRESION ########
    @_('expresion OP_LOG super_exp', 'expresion')
    def super_exp(self, p):
        return p

    @_('exp OP_REL exp', 'exp')
    def expresion(self, p):
        return p

    ####### EXP ########
    @_('termino OP_ARIT_SEC exp', 'termino')
    def exp(self, p):
        return p

    ####### TERMINO ########
    @_('factor OP_ARIT_PRIM termino', 'factor')
    def termino(self, p):
        return p

    ######## FACTOR ########
    @_('LP expresion RP','OP_ARIT_PRIM var_cte', 'var_cte')
    def factor(self, p):
        return p

    ######## VAR_CTE ########
    @_('ID', 'CTE_I', 'CTE_F', 'CTE_STRING')
    def var_cte(self, p):
        return p

    