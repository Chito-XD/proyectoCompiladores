from functionDirectory import FunctionDirectory
from memory import Memory
from utils.constants import (
    PROCESO, 
    PRINCIPAL, 
    OPER_ARIT_PRIM, 
    OPER_ARIT_SEC, 
    ERROR,
    VOID,
    OPER_LOG,
    OPER_REL,
    BOOLEANO
)
from utils.queue import Queue
from utils.stack import Stack
from utils.types import get_type_operation, get_cte_variable, get_type_from_address


class ManagerSemantic():

    def __init__(self):
        self.directory = FunctionDirectory()
        self.memory = Memory()
        self.currentType = None
        self.method_id = None
        self.class_id = None

        self.called_class = "" # clase que llamas ( called_class.ID() )
        self.called_method = "" # metodo que llamas ( called_class.called_method() )
        self.current_param = 1 # contador para asignar los parámetros en la llamada de un método
        self.currentVariables = Queue() # FI FO

        # Variables para cuadruplos
        self.operadores = Stack() #LI FO
        self.operandos = Stack()
        self.tipos = Stack()
        self.saltos = Stack()

        # Cuadruplos
        self.cuadruplo_counter = 1
        self.cuadruplos = []

    
    def set_current_type(self, var_type):
        print('El tipo actual es', var_type)
        self.currentType = var_type
    
    def set_method_id(self, curr_id):
        print('seteo', curr_id)
        self.memory.reset_local_memory()
        self.method_id = curr_id
    
    def set_class_id(self, class_id):
        print('la clase es', class_id)
        self.memory.reset_global_memory()
        self.class_id = class_id
    
    def create_class(self, class_name):
        print('creo clase', class_name)
        self.set_class_id(class_name)
        self.set_method_id(class_name)
        self.directory.createClass(class_name)
        params = {
            "tipo": PROCESO,
            "inicio": len(self.cuadruplos)
        }
        self.directory.createFunction(class_name, class_name, params)

    def create_function_directory(self):
        self.create_cruadruplo('Goto', None, None, 'main')
    
    def add_function(self, function_name):
        print("Se creo la funcion", function_name)
        self.set_method_id(function_name)
        params = {
            "tipo": self.currentType,
            "inicio": len(self.cuadruplos)
        }
        self.directory.createFunction(self.class_id, function_name, params)
    
    def set_called_class(self, class_name):
        self.called_class = class_name
    
    def clear_called_fun(self):
        self.called_class = ""
        self.called_method = ""
    
    def create_object_var(self, var_object):
        print("create OBJECT VAR")
        # TODO: 
        # var_object = self.operandos.pop()
        var = self.directory.get_variable(self.class_id, self.method_id, self.called_class)
        tipo_var = var["tipo"]
        
        print(var)
        atributo_var = self.directory.get_variable(tipo_var, tipo_var, var_object)
        address_atributo = atributo_var["direccion"]
        
        # self.called_class

        self.operandos.add(address_atributo)

    
    def create_era(self, method):
        print("create era")
        self.called_method = method

        if self.called_class == "":
            self.called_class = self.class_id

        self.current_param = 1
        # TODO: 
        
        dir_object_name = self.directory.get_address_object(self.class_id, self.method_id, self.called_class)
        # dir_object_name = self.called_class

        era_method = f"{dir_object_name}-{self.called_method}"

        self.create_cruadruplo("ERA", None, None, era_method)
    
    def evaluate_param(self):
        param = self.operandos.pop()
        self.create_cruadruplo('PARAM', param, None, self.current_param)
        self.current_param += 1

    def create_return(self):
        operando = self.operandos.pop()
        # TODO: Revisar que cuando se al metodo de una clase

        tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
        # tipo_retorno = self.directory.get_type_return(self.called_class, self.called_method, self.class_id)
        
        operando_type = get_type_from_address(operando)

        if operando_type == tipo_retorno:
            regresa_id = f"{self.class_id}-{self.method_id}"
            self.create_cruadruplo("REGRESA", regresa_id, None, operando)
        else:
            raise Exception(">> Return mismatch")
    
    def create_gosub(self):
        print("======create_gosub")
        dir_object_name = self.directory.get_address_object(self.class_id, self.method_id, self.called_class)
        # dir_object_name = self.called_class
        gosub_method = f"{dir_object_name}-{self.called_method}"
        self.create_cruadruplo("GOSUB", None, None, gosub_method)
        # TODO: Revisar que cuando se al metodo de una clase
        print("----")
        print(self.called_class, self.called_method, self.class_id, self.method_id)
        tipo_retorno = self.directory.get_type_return(self.called_class, self.called_method, self.class_id)
        print("TIPO RETORNO 3")
        print(tipo_retorno)

        if tipo_retorno != VOID:
            address = self.memory.set_memory_address(self.currentType, tipo_retorno)
            self.create_cruadruplo("=", gosub_method, None, address)
            self.operandos.add(address)

    def end_function(self):
        self.create_cruadruplo('END_FUNCTION', None, None, None)
    
    def create_principal(self):
        self.set_method_id(PRINCIPAL)
        params = {
            "tipo": PRINCIPAL,
            "inicio": len(self.cuadruplos)
        }
        tam = len(self.cuadruplos)
        self.cuadruplos[0] = ('Goto', None, None, tam)
        self.directory.createFunction(self.class_id, PRINCIPAL, params)
    
    # metodo para almacenar las variables en una cola hasta que encontemos su tipo
    def stash_variable(self, var):
        print("Añadiendo", var, "a la tabla de variables")
        if isinstance(var, tuple):
            var = var[1]
        self.currentVariables.add(var)
    
    # metodo que guarda las variablees del stash en el dir una vez que sabemos el tipo
    def store_variables(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.pop()
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            # print("00000000000000000000000000000000000000")
            # print(tipo_retorno)
            # self.directory.print_directory()
            address = self.memory.set_memory_address(self.currentType, tipo_retorno)
            params = {
                "key": var,
                "tipo": self.currentType,
                "direccion": address
            }
            self.directory.addLocalVariable(self.class_id, self.method_id, params)
        
    # Metodo similar a store_variables pero para los métodos
    def store_params(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.pop()
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            address = self.memory.set_memory_address(self.currentType, tipo_retorno)
            params = {
                "key": var,
                "tipo": self.currentType,
                "direccion": address
            }
            self.directory.addParam(self.class_id, self.method_id, params)
    
    def insert_operando(self, operando):
        print("voy a insertar ", operando)
        # verifica si el operando es cte
        tipo_operando = get_cte_variable(operando)
        if not tipo_operando:
            # como no es cte, optenemos el tipo y direccion de la variable en el dir
            var = self.directory.get_variable(self.class_id, self.method_id, operando)
            tipo_operando = var["tipo"]
            address = var["direccion"]
        else:
            # como es cte, solicitamos un dirreccion del rango de cte
            address = self.memory.get_cte_address(tipo_operando, operando)
        self.operandos.add(address)

        print(f"el tipo de {operando} es {tipo_operando}")
        self.tipos.add(tipo_operando)
    
    def insert_operador(self, operador):
        print("insert operador", operador)
        self.operadores.add(operador)
    
    # metodo que maneja el "fondo falso"
    def manage_back_operator(self, create=True):
        if create:
            self.operadores.add("(")
        else:
            self.operadores.pop()

    def create_cruadruplo(self, operator, op_izq, op_der, temporal):
        print("Creando cuadruplo (", operator, op_izq, op_der, temporal,")")
        self.cuadruplos.append((operator, op_izq, op_der, temporal))

    def create_cruadruplo_no_lin(self, goto, cond, destino):
        print("Creando cuadruplo nol lineal (", goto, cond, destino,")")
        self.cuadruplos.append((goto, cond, destino))

    def primary_arithmetic_operation(self):
        if self.operadores.peek() in OPER_ARIT_PRIM:
            self.arithmetic_ops()
    
    def secondary_arithmetic_operation(self):
        if self.operadores.peek() in OPER_ARIT_SEC:
            self.arithmetic_ops()
    
    def logical_operation(self):
        if self.operadores.peek() in OPER_LOG:
            self.arithmetic_ops()
    
    def relational_operation(self):
        if self.operadores.peek() in OPER_REL:
            self.arithmetic_ops()

    def arithmetic_ops(self):
        op = self.operadores.pop()
        op_der = self.operandos.pop()
        op_izq = self.operandos.pop()

        tipo_der = self.tipos.pop()
        tipo_izq = self.tipos.pop()

        operation_type = get_type_operation(tipo_izq, tipo_der, op)
        if operation_type is not ERROR:
            # result = f'temporal_{self.cuadruplo_counter}'
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            temporal_address = self.memory.set_memory_address(operation_type, tipo_retorno)

            self.cuadruplo_counter += 1
            self.create_cruadruplo(op, op_izq, op_der, temporal_address)
            self.operandos.add(temporal_address)
            self.tipos.add(operation_type)
        else:
            raise Exception(f"==> TYPE MISTMATCH - No se puede evaluar -> {op_izq} {op} {op_der}")

    def create_asignacion(self):
        res = self.operandos.pop()
        tipo_resultado = self.tipos.pop()
        lado_izq = self.operandos.pop()
        tipo_izq = self.tipos.pop()
        Operator = self.operadores.pop()

        operator_type = get_type_operation(tipo_resultado, tipo_izq, Operator)
        if operator_type is not ERROR:
            self.create_cruadruplo("=", res, None, lado_izq)
        else: 
            raise Exception("==> TYPE MISTMATCH - Ambos lados de la aisgnacion son de diferente tipo")
        

    def create_escritura(self):
        self.create_cruadruplo("ESCRIBE", None, None, self.operandos.peek())

    def create_escritura_exp(self):
        Res = self.operandos.pop()
        self.create_cruadruplo("ESCRIBE", None, None, Res)
    
    def create_lectura(self, op):
        if isinstance(op, tuple):
            op = op[1]
        var = self.directory.get_variable(self.class_id, self.method_id, op)
        self.create_cruadruplo("LECTURA", None, None, var["direccion"])
        
    
    def revisar_estatuo(self):
        self.arithmetic_ops()
        cond = self.operandos.pop()
        typeC = self.tipos.pop()
        
        if typeC == BOOLEANO:
            self.create_cruadruplo_no_lin("GotoF", cond, "?")
            Tam = len(self.cuadruplos)
            print("Tam:", Tam)
            self.saltos.add(Tam-1)
        else:
            raise Exception("Mismatch error")

    def end_estatuto(self):
        
        C1 = self.saltos.pop()
        Temp = self.cuadruplos[C1]
        N = len(self.cuadruplos)
        sN = str(N)

        Cont = 0
        
        for a in Temp:
            break

        for b in Temp:
            if Cont == 1:
                break
            
            Cont = Cont + 1

        self.cuadruplos[C1] = (a, b, sN)

    def goto_revisar(self):
        Falso = self.saltos.pop()
        Falso2 = self.cuadruplos[Falso]
        self.create_cruadruplo_no_lin("Goto", "ELSE", "?")
        Tam = len(self.cuadruplos)
        self.saltos.add(Tam-1)
        sTam = str(Tam)

        Cont = 0

        for a in Falso2:
            break

        for b in Falso2:
            if Cont == 1:
                break
            
            Cont = Cont + 1

        print("ELSE", a, b, sTam)

        self.cuadruplos[Falso] = (a, b, sTam)

    def meterActual(self):
        Tam = len(self.cuadruplos)
        self.saltos.add(Tam)
        self.saltos.add(Tam)

    def gotoWhile(self):
        self.arithmetic_ops()
        cond = self.operandos.pop()
        typeC = self.tipos.pop()
        
        if typeC == BOOLEANO:
            self.create_cruadruplo_no_lin("GotoF", cond, "?")
            Tam = len(self.cuadruplos)
            self.saltos.add(Tam-1)
        else:
            raise Exception("Mismatch error")

    def SaleWhile(self):
        Falso = self.saltos.pop()
        Falso2 = self.cuadruplos[Falso]
        RetNum = self.saltos.pop()
        # Ret = self.cuadruplos[RetNum]
        Tam = len(self.cuadruplos)
        sTam = str(Tam+1)

        Cont = 0

        for a in Falso2:
            break

        for b in Falso2:
            if Cont == 1:
                break
            
            Cont = Cont + 1

        self.create_cruadruplo_no_lin("Goto", None, RetNum)
        self.cuadruplos[Falso] = (a,b,sTam)

    def EntraFor(self):
        Tam = len(self.cuadruplos)
        self.saltos.add(Tam)

    def SaleFor(self):
        Reg = self.saltos.pop()
        self.create_cruadruplo_no_lin("gotoFor", None, Reg)


    
    