from sly import Parser
from lex import Lex
from managerSemantic import ManagerSemantic
class Yacc(Parser):
    
    tokens = Lex.tokens

    def __init__(self):
        self.names = {}
        self.manager = ManagerSemantic()

    
    ######## PROGRAMA ########
    @_('PROGRAMA ID createDirectory SEMICOLON dec_clas dec_vars dec_func principal',
       'PROGRAMA ID createDirectory SEMICOLON dec_clas dec_vars principal',
       'PROGRAMA ID createDirectory SEMICOLON dec_clas dec_func principal', 
       'PROGRAMA ID createDirectory SEMICOLON dec_clas principal',
       'PROGRAMA ID createDirectory SEMICOLON dec_vars dec_func principal', 
       'PROGRAMA ID createDirectory SEMICOLON dec_vars principal', 
       'PROGRAMA ID createDirectory SEMICOLON dec_func principal', 
       'PROGRAMA ID createDirectory SEMICOLON principal')
    def program(self, p):
        return p

    ######## PRINCIPAL ########
    @_('PRINCIPAL addPrincipal LP RP bloque printDirectory')
    def principal(self, p):
        return p
    
    ######## DEC_CLAS ########
    @_('CLASE ID HEREDA ID LK RK', 
       'CLASE ID LK RK')
    def dec_clas(self, p):
        print(p.HEREDA)
        return p
    
    # @_('ATRIBUTOS dec_vars_cicle METODOS dec_func', 
    #    'METODOS dec_func', 
    #    'ATRIBUTOS dec_vars_cicle')
    # def dec_clas_aux(self, p):
    #     return p

    ######## DEC_VARS ########
    @_('VARIABLES dec_vars_aux')
    def dec_vars(self, p):
        return p

    @_('dec_vars_aux2 DOTS tipo_simple SEMICOLON storeVariables dec_vars_aux',
       'dec_vars_aux2 DOTS tipo_simple SEMICOLON storeVariables',
       'dec_vars_aux2 DOTS tipo_compuesto SEMICOLON dec_vars_aux storeVariables',
       'dec_vars_aux2 DOTS tipo_compuesto SEMICOLON storeVariables')
    def dec_vars_aux(self, p):
        return p

    @_('var stashVar COMMA dec_vars_aux2',
       'var stashVar')
    def dec_vars_aux2(self, p):
        return p
    
    @_('ID LC CTE_I RC LC CTE_I RC',
       'ID LC CTE_I RC',
       'ID')
    def var(self, p):
        return p

    ######## PARAMETROS ########
    @_('ID stashVar DOTS tipo_simple storeVariables COMMA parametros', 
       'ID stashVar DOTS tipo_simple storeVariables')
    def parametros(self, p):
        return p
    
    ######## DEC_FUNC ########
    @_('tipo_simple FUNCION ID addFunction LP parametros RP SEMICOLON dec_vars bloque dec_func', 
       'tipo_simple FUNCION ID addFunction LP parametros RP SEMICOLON bloque dec_func',
       'tipo_simple FUNCION ID addFunction LP RP SEMICOLON dec_vars bloque dec_func',
       'tipo_simple FUNCION ID addFunction LP RP SEMICOLON bloque dec_func',
       'tipo_simple FUNCION ID addFunction LP parametros RP SEMICOLON dec_vars bloque', 
       'tipo_simple FUNCION ID addFunction LP parametros RP SEMICOLON bloque',
       'tipo_simple FUNCION ID addFunction LP RP SEMICOLON dec_vars bloque',
       'tipo_simple FUNCION ID addFunction LP RP SEMICOLON bloque',
       'VOID FUNCION ID addFunction LP parametros RP SEMICOLON dec_vars bloque dec_func', 
       'VOID FUNCION ID addFunction LP parametros RP SEMICOLON bloque dec_func',
       'VOID FUNCION ID addFunction LP RP SEMICOLON dec_vars bloque dec_func',
       'VOID FUNCION ID addFunction LP RP SEMICOLON bloque dec_func',
       'VOID FUNCION ID addFunction LP parametros RP SEMICOLON dec_vars bloque', 
       'VOID FUNCION ID addFunction LP parametros RP SEMICOLON bloque',
       'VOID FUNCION ID addFunction LP RP SEMICOLON dec_vars bloque',
       'VOID FUNCION ID addFunction LP RP SEMICOLON bloque')
    def dec_func(self, p):
        return p

    ######## BLOQUE ########
    @_('LK RK', 
       'LK bloque_aux RK')
    def bloque(self, p):
        return p
    
    @_('estatuto bloque_aux', 
       'estatuto')
    def bloque_aux(self, p):
        return p

    ######## ESTATUTO ########
    @_('asignacion', 
       'funcion SEMICOLON', 
       'retorno', 
       'lectura', 
       'escritura', 
       'decision', 
       'repeticion')
    def estatuto(self, p):
        return p

    ######## ASIGNACION ########
    @_('variable ASSIGN insertOperador super_exp crearAsignacion SEMICOLON')
    def asignacion(self, p):
        return p
    
    ######## LLAMADA FUNCION ########
    @_('ID LP funcion_aux RP')
    def funcion(self, p):
        return p
    
    @_('super_exp COMMA funcion_aux', 
       'super_exp')
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
    
    @_('super_exp create_escritura_exp COMMA escritura_aux', 
       'CTE_STRING create_escritura COMMA escritura_aux', 
       'super_exp create_escritura_exp', 
       'CTE_STRING create_escritura',)
    def escritura_aux(self, p):
        return p
    
    ######## LECTURA ########
    @_('LEE LP lectura_aux RP SEMICOLON')
    def lectura(self, p):
        return p
 
    @_('variable create_lectura COMMA lectura_aux', 
       'variable create_lectura')
    def lectura_aux(self, p):
        return p
    
    ####### DECISION ########
    @_('SI LP super_exp RP revisar_estatuto ENTONCES  bloque goto_revisar SINO bloque end_estatuto', 
       'SI LP super_exp RP revisar_estatuto ENTONCES bloque end_estatuto')
    def decision(self, p):
        return p
    
    ####### REPETICION ######## 
    # revisar el desde
    @_('MIENTRAS meterActual LP super_exp RP gotoWhile HACER bloque SaleWhile', 
       'DESDE ID ASSIGN super_exp HASTA super_exp HACER bloque')
    def repeticion(self, p):
        return p
    
    ######## TIPO ########
    @_('ENTERO setType', 
       'FLOTANTE setType', 
       'CHAR setType', 
       'BOOLEAN setType')
    def tipo_simple(self, p):
        return p
    
    @_('ID setType')
    def tipo_compuesto(self, p):
        return p

    ####### SUPER EXPRESION ########
    @_('expresion logicalOperation OP_LOG insertOperador super_exp', 
       'expresion logicalOperation')
    def super_exp(self, p):
        return p

    ####### EXPRESION ########
    @_('exp relationalOperation OP_REL insertOperador exp', 
       'exp relationalOperation')
    def expresion(self, p):
        return p

    ####### EXP ########
    @_('termino secondaryOperation OP_ARIT_SEC insertOperador exp', 
       'termino secondaryOperation')
    def exp(self, p):
        return p

    ####### TERMINO ########
    @_('factor primaryOperation OP_ARIT_PRIM insertOperador termino', 
       'factor primaryOperation')
    def termino(self, p):
        return p

    ######## FACTOR ########
    @_('LP super_exp RP',
       'var_cte',
       'variable',
       'funcion')
    def factor(self, p):
        return p

    ######## VAR_CTE ########
    @_('CTE_I insertOperando', 
       'CTE_F insertOperando', 
       'CTE_STRING insertOperando')
    def var_cte(self, p):
        return p
    
    ######## VARIABLE ########
    @_('ID LC super_exp RC LC super_exp RC',
       'ID LC super_exp RC',
       'ID DOT ID',
       'ID DOT ID LP variable_aux RP',
       'ID insertOperando')
    def variable(self, p):
        return p
    
    @_('super_exp COMMA variable_aux', 
       'super_exp')
    def variable_aux(self, p):
        return p


######## PUNTOS NEURALGICOS ######## 
    @_('createDirectory :')
    def createDirectory(self, p):
        self.manager.create_function_directory(p[-1])

    @_('addFunction :')
    def addFunction(self, p):
        self.manager.add_function(p[-1])
    
    @_('addPrincipal :')
    def addPrincipal(self, p):
        self.manager.create_principal()

    @_('stashVar :')
    def stashVar(self, p):
        self.manager.stash_variable(p[-1])

    @_('setType :')        
    def setType(self, p):
        self.manager.set_current_type(p[-1])

    @_('storeVariables :')
    def storeVariables(self, p):
        self.manager.store_variables()

    @_('printDirectory :')
    def printDirectory(self, p):
        self.manager.print_directory()
    
    @_('insertOperador :')
    def insertOperador(self, p):
        self.manager.insert_operador(p[-1])
    
    @_('logicalOperation :')
    def logicalOperation(self, p):
        self.manager.logical_operation()
    
    @_('relationalOperation :')
    def relationalOperation(self, p):
        self.manager.relational_operation()
    
    @_('secondaryOperation :')
    def secondaryOperation(self, p):
        self.manager.secondary_arithmetic_operation()

    @_('primaryOperation :')
    def primaryOperation(self, p):
        self.manager.primary_arithmetic_operation()

    @_('insertOperando :')
    def insertOperando(self, p):
        self.manager.insert_operando(p[-1])

    @_('crearAsignacion :')
    def crearAsignacion(self, p):
        self.manager.create_asignacion()

    #Revisar por que da error
    @_('create_escritura :')
    def create_escritura(self, p):
        self.manager.create_escritura(p[-1])

    @_('create_escritura_exp :')
    def create_escritura_exp(self, p):
        self.manager.create_escritura_exp()

    #Revisar
    @_('create_lectura :')
    def create_lectura(self, p):
        self.manager.create_lectura(p[-1])

    @_('revisar_estatuto :')
    def revisar_estatuto(self, p):
        self.manager.revisar_estatuo()

    @_('end_estatuto :')
    def end_estatuto(self, p):
        self.manager.end_estatuto()

    @_('goto_revisar :')
    def goto_revisar(self, p):
        self.manager.goto_revisar()
    
    @_('meterActual :')
    def meterActual(self, p):
        self.manager.meterActual()

    @_('gotoWhile :')
    def gotoWhile(self, p):
        self.manager.gotoWhile()

    @_('SaleWhile :')
    def SaleWhile(self, p):
        self.manager.SaleWhile()