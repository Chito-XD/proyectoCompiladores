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
    BOOLEANO,
    ENTERO
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
        
        self.called_methods_stack = Stack()
        self.called_method = ""
        self.params_stack = Stack()

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
    
    def create_era(self, method):
        print("Method: " + method)
        self.called_methods_stack.add(method)
        self.called_method = self.called_methods_stack.peek()
        self.create_cruadruplo("ERA", None, None, method)
        # Añadir un arreglo de params
        self.params_stack.add([])
        
    
    def evaluate_params(self):
        function_params = self.directory.returnParam(self.class_id, self.called_method)
        print("Clase: " + self.class_id)
        print("Metodo: " + self.called_method)
        print("Num Param " + str(len(function_params)))

        given_params = self.params_stack.pop()
        print("Given params", len(given_params))

        if len(function_params) == len(given_params) :

            for i in range(len(given_params)):
                print(given_params[i])
                tipo = get_type_from_address(given_params[i])

                if tipo == function_params[i]:
                    self.create_cruadruplo('PARAM', given_params[i], None, i)
                else:
                    raise Exception("Mismatch type in parameters")

        else:
            raise Exception(f"Function expects {len(function_params)} parameters. {len(self.given_params)} given")
        
    
    # [
    #     [], fibo
    #     [], fact
    # ]
    # stashea los parametros de la pila de operandos en un stack de arreglos 
    # Cada arreglo contiene los parámteros de cada función en caso que estén encadenadas
    def stashParams(self):
        param = self.operandos.pop()
        top_param = self.params_stack.pop()
        top_param.append(param)
        self.params_stack.add(top_param)

    def create_return(self):
        operando = self.operandos.pop()
        # TODO: Revisar que cuando se al metodo de una clase
        tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
        operando_type = get_type_from_address(operando)

        if operando_type == tipo_retorno:
            self.create_cruadruplo("REGRESA", self.method_id, None, operando)
        else:
            raise Exception(">> Return mismatch")
    
    def create_gosub(self):
        self.create_cruadruplo("GOSUB", None, None, self.called_method)
        # TODO: Revisar que cuando se al metodo de una clase
        tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.called_method)
        if tipo_retorno != VOID:
            address = self.memory.set_memory_address(self.currentType, tipo_retorno)
            self.create_cruadruplo("=", self.called_method, None, address)
            # print(">>>>>>>>>>>>>>> GOSUB", address)
            self.operandos.add(address)
            tipo = get_type_from_address(address)
            self.tipos.add(tipo)

        self.called_methods_stack.pop()
        self.called_method = self.called_methods_stack.peek()

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
    
    def stash_variable(self, var):
        print("Añadiendo", var, "a la tabla de variables")
        self.currentVariables.add(var)
    
    def store_variables(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.pop()
            if len(var) == 5: #  arreglo
                dim = {
                    "dim1": var[3]
                }
                var_size = int(var[3])
            elif len(var) == 8: # matriz
                dim = {
                    "dim1": var[3],
                    "dim2": var[6]
                }
                var_size = int(var[3]) * int(var[6])
            else: # variable normal
                dim = None
                var_size = 1
            var = var[1]

            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            address = self.memory.set_memory_address(self.currentType, tipo_retorno, var_size)
            params = {
                "key": var,
                "tipo": self.currentType,
                "direccion": address,
                "dimension": dim
            }
            self.directory.addLocalVariable(self.class_id, self.method_id, params)
        
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
    
    def update_variable(self, var, value):
        params = {
            "key": var,
            "value": value
        }
        self.directory.updateVariable(self.class_id, self.method_id, params)
    
    def verifica_dim(self, dim):
        dimensions = Stack()
        for _ in range(dim):
            dimensions.add(self.operandos.pop()) # dimensions = al reves =  dim2 dim1
            self.tipos.pop()
        
        operando_address = self.operandos.pop() # id
        self.tipos.pop()

        print(operando_address, self.class_id, self.method_id)

        the_var = self.directory.find_var_from_address(self.class_id, self.method_id, operando_address)

        print("the_var", the_var)

        var_dimension = the_var["dimension"]
        
        # Validate the dimensions of the var with the given dimension
        if var_dimension.get("dim2") and dim == 1:
            raise Exception("Missing dimension declaration")
        if not var_dimension.get("dim2") and dim == 2:
            raise Exception("Extra dimension declaration")

        # DirBase() + s1*d2 + s2
        # the_var["direccion"] * 
        # 1010 + s1(45 tambien es direccion) => cambiar addres a valores
        # 1015

        if dim == 1:
            superior_limit = var_dimension["dim1"]
            superior_limit_address = self.memory.get_cte_address(ENTERO, superior_limit)
            zero_addres = self.memory.get_cte_address(ENTERO, 0)
            dim_operando = dimensions.pop()
            self.create_cruadruplo('VERIFICA', dim_operando, zero_addres, superior_limit_address)
            temporal_address2 = dim_operando
        elif dim == 2:
            for i in range(dim):
                superior_limit = var_dimension[f"dim{(i+1)}"]

                superior_limit_address = self.memory.get_cte_address(ENTERO, superior_limit)
                zero_addres = self.memory.get_cte_address(ENTERO, 0)

                dim_operando = dimensions.pop()
                self.create_cruadruplo('VERIFICA', dim_operando, zero_addres, superior_limit_address)
                if i == 0:
                    temporal_address = self.memory.set_memory_address(ENTERO, None)
                    m1 = superior_limit_address = self.memory.get_cte_address(ENTERO, var_dimension["dim2"])
                    self.create_cruadruplo('*', dim_operando, m1, temporal_address)
                else:
                    temporal_address2 = self.memory.set_memory_address(ENTERO, None)
                    self.create_cruadruplo('+', temporal_address , dim_operando, temporal_address2)


        temporal_address3 = self.memory.set_memory_address(ENTERO, None)
        temporal_address3 = f"({temporal_address3})"
        base_dir = f"dir-{the_var['direccion']}"
        self.create_cruadruplo("+", base_dir, temporal_address2, temporal_address3)
        self.operandos.add(temporal_address3)
        self.tipos.add(the_var["tipo"])
        

    def insert_operando(self, operando):
        print("voy a insertar ", operando)
        tipo_operando = get_cte_variable(operando)
        if not tipo_operando:
            var = self.directory.get_variable(self.class_id, self.method_id, operando)
            tipo_operando = var["tipo"]
            address = var["direccion"]
        else:
            address = self.memory.get_cte_address(tipo_operando, operando)

        self.operandos.add(address)

        print(f"el tipo de {operando} es {tipo_operando}")
        self.tipos.add(tipo_operando)
    
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
        # if isinstance(op, tuple):
        #     op = op[1]
        # var = self.directory.get_variable(self.class_id, self.method_id, op)
        var = self.operandos.pop()
        self.tipos.pop()
        self.create_cruadruplo("LECTURA", None, None, var)
        
    
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

    def SaleFor(self):
        Reg = self.saltos.pop()
        Reg2 = self.saltos.pop()
        Aux = Reg2
        self.create_cruadruplo_no_lin("Goto", None, Aux)
        Temp = self.cuadruplos[Reg]
        N = len(self.cuadruplos)
        sN = str(N)

        Cont = 0
        
        for a in Temp:
            break

        for b in Temp:
            if Cont == 1:
                break
            
            Cont = Cont + 1


        self.cuadruplos[Reg] = (a, b, sN)


    def igualdadFor(self):
        ladoder = self.operandos.pop()
        ladoizq = self.operandos.pop()
        tipoder = self.tipos.pop()
        tipoizq = self.tipos.pop()

        operation_type = get_type_operation(tipoizq, tipoder, "<=")
        if operation_type is not ERROR:
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            temporal_address = self.memory.set_memory_address(operation_type, tipo_retorno)
            self.create_cruadruplo("<=", ladoizq, ladoder, temporal_address)
            self.operandos.add(ladoizq)
            self.tipos.add(tipoizq)

            Aux = len(self.cuadruplos)
            self.saltos.add(Aux)

            self.create_cruadruplo_no_lin("GotoF", temporal_address, "?")

    def sumaFor(self):
        cont = self.operandos.pop()
        tipo = self.tipos.pop()

        operation_type = get_type_operation(tipo, ENTERO, "+")
        if operation_type is not ERROR:
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            temporal_address = self.memory.set_memory_address(operation_type, tipo_retorno)
            Suma = self.memory.get_cte_address(ENTERO, 1)
            self.create_cruadruplo("+", cont, Suma, temporal_address)
            self.create_cruadruplo("=", temporal_address, None, cont)


    def create_asignacionLoop(self):
            print("Crear asignacion")
            res = self.operandos.pop()
            tipo_resultado = self.tipos.pop()
            lado_izq = self.operandos.pop()
            tipo_izq = self.tipos.pop()
            Operator = self.operadores.pop()

            operator_type = get_type_operation(tipo_resultado, tipo_izq, Operator)
            if operator_type is not ERROR:
                self.create_cruadruplo("=", res, None, lado_izq)
                self.operandos.add(lado_izq)
                self.tipos.add(tipo_izq)

                Aux = len(self.cuadruplos)
                self.saltos.add(Aux)

                


    
    