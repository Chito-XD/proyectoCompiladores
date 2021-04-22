from sly import Parser
from lex import Lex
from functionDirectory import FunctionDirectory
dire = FunctionDirectory()

class Yacc(Parser):
    
    tokens = Lex.tokens

    def __init__(self):
        self.names = {}

    
    ######## PROGRAMA ########
    @_('PROGRAMA ID SEMICOLON dec_clas dec_vars dec_func principal','PROGRAMA ID SEMICOLON dec_clas dec_vars principal','PROGRAMA ID SEMICOLON dec_clas dec_func principal', 'PROGRAMA ID SEMICOLON dec_clas principal','PROGRAMA ID SEMICOLON dec_vars dec_func principal', 'PROGRAMA ID SEMICOLON dec_vars principal', 'PROGRAMA ID SEMICOLON dec_func principal', 'PROGRAMA ID SEMICOLON principal')
    def program(self, p):
        return p
    
    ######## PRINCIPAL ########
    @_('PRINCIPAL LP RP bloque')
    def principal(self, p):
        return p
    
    ######## DEC_CLAS ########
    @_('CLASE ID HEREDA ID LK dec_clas_aux RK', 'CLASE ID LK dec_clas_aux RK', 'CLASE ID HEREDA ID LK RK', 'CLASE ID LK RK')
    def dec_clas(self, p):
        return p
    
    @_('ATRIBUTOS dec_vars_cicle METODOS dec_func', 'METODOS dec_func', 'ATRIBUTOS dec_vars_cicle')
    def dec_clas_aux(self, p):
        return p

    ######## DEC_VARS ########
    @_('VARIABLES dec_vars_cicle')
    def dec_vars(self, p):
        return p
    
    @_('dec_vars_aux DOTS tipo SEMICOLON dec_vars_cicle', 'dec_vars_aux DOTS tipo SEMICOLON')
    def dec_vars_cicle(self, p):
        return p
    
    @_('ID COMMA dec_vars_aux', 'ID')
    def dec_vars_aux(self, p):
        return p

    ######## PARAMETROS ########
    @_('ID DOTS tipo COMMA parametros', 'ID DOTS tipo')
    def parametros(self, p):
        return p
    
    ######## DEC_FUNC ########
    @_('tipo FUNCION ID LP parametros RP SEMICOLON dec_vars bloque', 'tipo FUNCION ID LP parametros RP SEMICOLON bloque','tipo FUNCION ID LP RP SEMICOLON dec_vars bloque','tipo FUNCION ID LP RP SEMICOLON bloque','tipo FUNCION ID LP parametros RP SEMICOLON dec_vars bloque dec_func', 'tipo FUNCION ID LP parametros RP SEMICOLON bloque dec_func','tipo FUNCION ID LP RP SEMICOLON dec_vars bloque dec_func','tipo FUNCION ID LP RP SEMICOLON bloque dec_func')
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
    @_('asignacion', 'funcion SEMICOLON', 'retorno', 'lectura', 'escritura', 'decision', 'repeticion')
    def estatuto(self, p):
        return p

    ######## ASIGNACION ########
    @_('ID ASSIGN super_exp SEMICOLON', 'ID ASSIGN funcion asignacion_aux', 'ID ASSIGN funcion SEMICOLON')
    def asignacion(self, p):
        return p
    
    @_('super_exp asignacion_aux', 'super_exp')
    def asignacion_aux(self, p):
        return p
    
    ######## LLAMADA FUNCION ########
    @_('ID LP funcion_aux RP', 'ID LP RP')
    def funcion(self, p):
        return p
    
    @_('super_exp COMMA funcion_aux', 'super_exp')
    def funcion_aux(self, p):
        return p

    ######## RETORNO ########
    @_('REGRESA LP super_exp RP SEMICOLON')
    def retorno(self, p):
        return p
    
    ####### ESCRITURA ########
    @_('ESCRIBE LP escritura_aux RP SEMICOLON')
    def escritura(self, p):
        return p
    
    @_('super_exp COMMA escritura_aux', 'CTE_STRING COMMA escritura_aux', 'super_exp', 'CTE_STRING',)
    def escritura_aux(self, p):
        return p
    
    ######## LECTURA ########
    @_('LEE LP lectura_aux RP SEMICOLON')
    def lectura(self, p):
        return p

    @_('lectura_aux_vars COMMA lectura_aux', 'lectura_aux_vars')
    def lectura_aux(self, p):
        return p
    
    @_('class_var', 'ID')
    def lectura_aux_vars(self, p):
        return p

    ####### DECISION ########
    @_('SI LP super_exp RP ENTONCES bloque SINO bloque', 'SI LP super_exp RP ENTONCES bloque')
    def decision(self, p):
        return p
    
    ####### REPETICION ######## 
    # revisar el desde
    @_('MIENTRAS LP super_exp RP HACER bloque', 'DESDE ID ASSIGN super_exp HASTA super_exp HACER bloque')
    def repeticion(self, p):
        return p
    
    ######## TIPO ########
    @_('ENTERO', 'FLOTANTE', 'CHAR', 'VOID', 'BOOLEAN' 'ID')
    def tipo(self, p):
        return p

    ####### SUPER EXPRESION ########
    @_('expresion OP_LOG super_exp', 'expresion')
    def super_exp(self, p):
        return p

    ####### EXPRESION ########
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
    @_('LP super_exp RP','OP_ARIT_PRIM var_cte', 'var_cte')
    def factor(self, p):
        return p

    ######## VAR_CTE ########
    @_('funcion', 'class_method' ,'class_var', 'ID', 'CTE_I', 'CTE_F', 'CTE_STRING')
    def var_cte(self, p):
        return p

    ######## CLASS_METHOD ########
    @_('ID DOT funcion')
    def class_method(self, p):
        return p
    
    ######## CLASS_VAR ########
    @_('ID DOT ID')
    def class_var(self, p):
        return p


    