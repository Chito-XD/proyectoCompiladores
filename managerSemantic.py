from functionDirectory import FunctionDirectory
from memory import Memory
from utils.constants import (
    PROCESO, 
    PRINCIPAL, 
    OPER_ARIT_PRIM, 
    OPER_ARIT_SEC, 
    ERROR,
    OPER_LOG,
    OPER_REL,
    BOOLEANO
)
from utils.queue import Queue
from utils.stack import Stack
from utils.types import get_type_operation, evaluate_operation, get_type_variable


class ManagerSemantic():

    def __init__(self):
        self.directory = FunctionDirectory()
        self.memory = Memory()
        self.currentType = None
        self.method_id = None
        self.called_method = ""
        self.current_param = 1
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
    
    def create_function_directory(self, program_id):
        print("Se crea directorio", program_id)
        self.set_method_id(program_id)
        params = {
            "tipo": PROCESO,
            "inicio": 0
        }
        self.create_cruadruplo('Goto', None, None, 'main')
        self.directory.createFunction(program_id, params)
    
    def add_function(self, function_name):
        print("Se creo la funcion", function_name)
        self.set_method_id(function_name)
        params = {
            "tipo": self.currentType,
            "inicio": len(self.cuadruplos)
        }
        self.directory.createFunction(function_name, params)
    
    def create_era(self, method):
        self.called_method = method
        self.current_param = 1
        self.create_cruadruplo("ERA", None, None, method)
    
    def evaluate_param(self):
        param = self.operandos.pop()
        self.create_cruadruplo('PARAM', param, None, self.current_param)
        self.current_param += 1

    
    def create_gosub(self):
        self.create_cruadruplo("GOSUB", None, None, self.called_method)

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
        self.directory.createFunction(PRINCIPAL, params)
    
    def stash_variable(self, var):
        print("Añadiendo", var, "a la tabla de variables")
        if isinstance(var, tuple):
            var = var[1]
        self.currentVariables.add(var)
    
    def store_variables(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.pop()
            address = self.memory.set_memory_address(self.currentType, self.directory.directory[self.method_id])
            params = {
                "key": var,
                "tipo": self.currentType,
                "direccion": address
            }
            self.directory.addLocalVariable(self.method_id, params)
        
    def store_params(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.pop()
            address = self.memory.set_memory_address(self.currentType, self.directory.directory[self.method_id])
            params = {
                "key": var,
                "tipo": self.currentType,
                "direccion": address
            }
            self.directory.addParam(self.method_id, params)
            # self.directory.addLocalVariable(self.method_id, params)
    
    def update_variable(self, var, value):
        params = {
            "key": var,
            "value": value
        }
        self.directory.updateVariable(self.method_id, params)

    def insert_operando(self, operando):
        print("voy a insertar ", operando)
        self.operandos.add(operando)
        tipo_op = get_type_variable(operando)
        if not tipo_op:
            var = self.directory.get_variable(self.method_id, operando)
            tipo_op = var["tipo"]
        print(f"el tipo de {operando} es {tipo_op}")
        self.tipos.add(tipo_op)
    
    def insert_operador(self, operador):
        print("insert operador", operador)
        self.operadores.add(operador)
    
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
        # print("primary")
        if self.operadores.peek() in OPER_ARIT_PRIM:
            self.arithmetic_ops()
    
    def secondary_arithmetic_operation(self):
        # print('secondary')
        if self.operadores.peek() in OPER_ARIT_SEC:
            self.arithmetic_ops()
    
    def logical_operation(self):
        # print('logical')
        if self.operadores.peek() in OPER_LOG:
            self.arithmetic_ops()
    
    def relational_operation(self):
        # print('relational')
        if self.operadores.peek() in OPER_REL:
            print("Operator:", self.operadores.peek())
            self.arithmetic_ops()

    def arithmetic_ops(self):
        op = self.operadores.pop()
        op_der = self.operandos.pop()
        op_izq = self.operandos.pop()

        tipo_der = self.tipos.pop()
        tipo_izq = self.tipos.pop()

        operation_type = get_type_operation(tipo_izq, tipo_der, op)
        if operation_type is not ERROR:
            # result = evaluate_operation(op_izq, op_der, op)
            result = f'temporal_{self.cuadruplo_counter}'
            self.cuadruplo_counter += 1
            self.create_cruadruplo(op, op_izq, op_der, result)
            self.operandos.add(result)
            self.tipos.add(operation_type)
        else:
            raise Exception(f"No se puede evaluar -> {op_izq} {op} {op_der}")

    def create_asignacion(self):
        print("Crear asignacion")
        res = self.operandos.pop()
        tipo_resultado = self.tipos.pop()
        lado_izq = self.operandos.pop()
        tipo_izq = self.tipos.pop()
        Operator = self.operadores.pop()

        operator_type = get_type_operation(tipo_resultado, tipo_izq, Operator)
        if operator_type is not ERROR:
            self.create_cruadruplo("=", res, None, lado_izq)
        

    def create_escritura(self):
        self.create_cruadruplo("ESCRIBE", None, None, self.operandos.peek())

    def create_escritura_exp(self):
        Res = self.operandos.pop()
        self.create_cruadruplo("ESCRIBE", None, None, Res)

    
    def create_lectura(self, op):
        if isinstance(op, tuple):
            op = op[1]
        self.directory.get_variable(self.method_id, op)
        self.create_cruadruplo("LECTURA", None, None, op)
        
    
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


    def print_directory(self):
        print("")
        for key in self.directory.directory.keys():
            print('function ---> ', key)
            print(self.directory.directory[key])
            var = self.directory.directory[key]["directorio_variables"].variables
            print(var)
            print("")
       
        cont = 0
        
        for cu in self.cuadruplos:
            print(cont, cu)
            cont = cont+1


    
    