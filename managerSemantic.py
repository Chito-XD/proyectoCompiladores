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

        self.called_objects_stack = Stack()
        self.called_object = None
        
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

    # Setea el tipo actual en la sintaxis
    def set_current_type(self, var_type):
        self.currentType = var_type
    
    # setear el metodo actual de la sintaxis
    def set_method_id(self, curr_id):
        self.memory.reset_local_memory()
        self.method_id = curr_id
    
    # setear la clase en la que se está compilando
    def set_class_id(self, class_id):
        self.memory.reset_global_memory()
        self.class_id = class_id
    
    # crear una clase en el directorio de funciones
    def create_class(self, class_name):
        self.set_class_id(class_name)
        self.set_method_id(class_name)
        self.directory.createClass(class_name)
        params = {
            "tipo": PROCESO,
            "inicio": len(self.cuadruplos)
        }
        self.directory.createFunction(class_name, class_name, params)

    # creat una funcion en el directorio de funciones
    def create_function_directory(self):
        self.create_cruadruplo('Goto', None, None, 'main')
    
    # añadir una funcion al directorio
    def add_function(self, function_name):
        # print("Se creo la funcion", function_name)
        self.set_method_id(function_name)
        params = {
            "tipo": self.currentType,
            "inicio": len(self.cuadruplos)
        }
        self.directory.createFunction(self.class_id, function_name, params)
    
    # guardar el nombre del objeto al que se esta llamando
    def set_called_class(self, called_object):
        # print("seteo la clase", called_object)
        self.called_objects_stack.add(called_object)
        self.called_object = called_object
    
    # metodo para crear el cuadruplo de una llamada a funcion
    def create_era(self, method):
        # print("Method: " + method)
        self.called_methods_stack.add(method)
        self.called_method = method

        # si la funcion que se llama es de la funcion principal
        if not self.called_object:
            self.create_cruadruplo("ERA", None, None, method)
        else:
            # si la funcion que se llama es de un objeto
            var_info = self.directory.get_var_info(self.class_id, self.method_id, self.called_object)
            class_name = var_info["tipo"]
            era_class = f"{class_name}-{method}"
            self.create_cruadruplo("ERA", None, None, era_class)

        # Añadir un arreglo de params
        self.params_stack.add([])
        
    # evaluar la cantidad y tipos de paramatros que se recibe y a los que se quiere mandar en la llamada a funcion
    def evaluate_params(self):

        class_name = self.class_id
        
        if self.called_object:
            var_info = self.directory.get_var_info(self.class_id, self.method_id, self.called_object)
            class_name = var_info["tipo"]
        
        function_params = self.directory.returnParam(class_name, self.called_method)
        
        given_params = self.params_stack.pop()

        if len(function_params) == len(given_params) :

            for i in range(len(given_params)):
                tipo = get_type_from_address(given_params[i])

                if tipo == function_params[i]:
                    self.create_cruadruplo('PARAM', given_params[i], None, i)
                else:
                    raise Exception("Mismatch type in parameters")

        else:
            raise Exception(f"Function expects {len(function_params)} parameters. {len(given_params)} given")
        
    
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

    # crear cuadruplo de return
    def create_return(self):
        operando = self.operandos.pop()
        
        if not self.called_object:
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.method_id)
            regresa_label = self.method_id
        else:
            var_info = self.directory.get_var_info(self.class_id, self.method_id, self.called_object)
            class_name = var_info["tipo"]
            tipo_retorno = self.directory.get_tipo_retorno(class_name, self.method_id)
            regresa_label = f"{self.called_object}-{self.method_id}"

        operando_type = get_type_from_address(operando)

        if operando_type == tipo_retorno:
            self.create_cruadruplo("REGRESA", regresa_label, None, operando)
        else:
            raise Exception(">> Return mismatch")
    
    # create cuadruplo de gosub
    def create_gosub(self):
        if not self.called_object:
            self.create_cruadruplo("GOSUB", None, None, self.called_method)
            gosub_class = self.called_method
            tipo_retorno = self.directory.get_tipo_retorno(self.class_id, self.called_method)
        else:
            var_info = self.directory.get_var_info(self.class_id, self.method_id, self.called_object)
            class_name = var_info["tipo"]
            tipo_retorno = self.directory.get_tipo_retorno(class_name, self.called_method)

            gosub_class = f"{class_name}-{self.called_method}"
            self.create_cruadruplo("GOSUB", None, None, gosub_class)
        
        # revisar si el tipo de retorno
        # si sí, crear el parche "guadalupano"
        if tipo_retorno != VOID:
            address = self.memory.set_memory_address(self.currentType, tipo_retorno)
            self.create_cruadruplo("=", self.called_method, None, address)
            self.operandos.add(address)
            tipo = get_type_from_address(address)
            self.tipos.add(tipo)

        self.called_methods_stack.pop()
        self.called_method = self.called_methods_stack.peek()

        self.called_objects_stack.pop()
        self.called_object = self.called_objects_stack.peek()

    # crear funcion para end function
    def end_function(self):
        self.create_cruadruplo('END_FUNCTION', None, None, None)
    
    # crear metodo principal del programa
    def create_principal(self):
        self.set_method_id(PRINCIPAL)
        params = {
            "tipo": PRINCIPAL,
            "inicio": len(self.cuadruplos)
        }
        tam = len(self.cuadruplos)
        self.cuadruplos[0] = ('Goto', None, None, tam)
        self.directory.createFunction(self.class_id, PRINCIPAL, params)
    
    # guardar en un stack las variables para despues guardarlas
    def stash_variable(self, var):
        self.currentVariables.add(var)
    
    # guardar en el directorio de variables las variables stasheadas
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
        
    # guardar los parametros en la tabla de variables del metodo en el que estas
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
    
    # metodo para verificar las dimensiones de la variable y comprobar si coinciden
    def verifica_dim(self, dim):
        dimensions = Stack()
        for _ in range(dim):
            dimensions.add(self.operandos.pop()) # dimensions = al reves =  dim2 dim1
            self.tipos.pop()

        
        operando_address = self.operandos.pop() # id
        self.tipos.pop()


        the_var = self.directory.find_var_from_address(self.class_id, self.method_id, operando_address)


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
        self.operadores.pop()
        
    # metodo para insertar un operador.
    # Se le asigna una direccion de memoria para ello
    def insert_operando(self, operando):
        # print("voy a insertar ", operando)
        tipo_operando = get_cte_variable(operando)
        if not tipo_operando:
            var = self.directory.get_variable(self.class_id, self.method_id, operando)
            tipo_operando = var["tipo"]
            address = var["direccion"]
        else:
            address = self.memory.get_cte_address(tipo_operando, operando)

        self.operandos.add(address)

        self.tipos.add(tipo_operando)

    # metodo para insertar un operador.
    # Se le asigna una direccion de memoria para ello y un fondo falso
    def insert_operandoArr(self, operando):
        tipo_operando = get_cte_variable(operando)
        if not tipo_operando:
            var = self.directory.get_variable(self.class_id, self.method_id, operando)
            tipo_operando = var["tipo"]
            address = var["direccion"]
        else:
            address = self.memory.get_cte_address(tipo_operando, operando)
        
        #Set fondo falso

        self.operadores.add('[')

        self.operandos.add(address)

        self.tipos.add(tipo_operando)
    
    # añadir el operador a la pila de operadores
    def insert_operador(self, operador):
        self.operadores.add(operador)
    
    # metodo para manejar la logica del fondo falso
    def manage_back_operator(self, create=True):
        if create:
            self.operadores.add("(")
        else:
            self.operadores.pop()

    # metodo para añadir al arreglo de los cuadruplo la tupla
    def create_cruadruplo(self, operator, op_izq, op_der, temporal):
        self.cuadruplos.append((operator, op_izq, op_der, temporal))

    # metodo para añadir al arreglo de los cuadruplo la tupla
    def create_cruadruplo_no_lin(self, goto, cond, destino):
        self.cuadruplos.append((goto, cond, destino))

    # punto para evaluar los operadores aritmeticos de multiplicacion y division
    def primary_arithmetic_operation(self):
        if self.operadores.peek() in OPER_ARIT_PRIM:
            self.arithmetic_ops()
    
    # punto para evaluar los operadores aritmeticos de suma y resta
    def secondary_arithmetic_operation(self):
        if self.operadores.peek() in OPER_ARIT_SEC:
            self.arithmetic_ops()
    
    # punto para evaluar los operadores logicos
    def logical_operation(self):
        if self.operadores.peek() in OPER_LOG:
            self.arithmetic_ops()
    
    # punto para evaluar los operadores relacionales
    def relational_operation(self):
        if self.operadores.peek() in OPER_REL:
            self.arithmetic_ops()

    # metodo para evaluar la operacion. Revisar en el cubo semantico y crear la variable temporal
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

    # metodo para crear el cuadruplo de asignacion
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
        
    # metodo para crear cuadruplo de escritura de super_exp
    def create_escritura(self):
        self.create_cruadruplo("ESCRIBE", None, None, self.operandos.pop())

    # meotod para crear el cuadruplo de escirutar normal
    def create_escritura_exp(self):
        Res = self.operandos.pop()
        self.create_cruadruplo("ESCRIBE", None, None, Res)
    
    # metodo para crear el cuadruplo de lectura
    def create_lectura(self, op):
        var = self.operandos.pop()
        self.tipos.pop()
        self.create_cruadruplo("LECTURA", None, None, var)
        
    
    def revisar_estatuo(self):
        cond = self.operandos.pop()
        typeC = self.tipos.pop()
        
        if typeC == BOOLEANO:
            self.create_cruadruplo_no_lin("GotoF", cond, "?")
            Tam = len(self.cuadruplos)
            # print("Tam:", Tam)
            self.saltos.add(Tam-1)
        else:
            raise Exception("Mismatch error")

    def end_estatuto(self):
        
        fin = self.saltos.pop()

        goto_command = self.cuadruplos[fin][0]
        goto_cond = self.cuadruplos[fin][1]
        
        self.cuadruplos[fin] = (goto_command, goto_cond, len(self.cuadruplos))


    def goto_revisar(self):
        Falso = self.saltos.pop()

        self.create_cruadruplo_no_lin("Goto", "ELSE", "?")

        Tam = len(self.cuadruplos)
        self.saltos.add(Tam-1)


        goto_command = self.cuadruplos[Falso][0]
        goto_cond = self.cuadruplos[Falso][1]

        self.cuadruplos[Falso] = (goto_command, goto_cond, Tam)

    def meterActual(self):
        Tam = len(self.cuadruplos)
        self.saltos.add(Tam)

    def gotoWhile(self):
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
        RetNum = self.saltos.pop()

        self.create_cruadruplo_no_lin("Goto", None, RetNum)

        goto_command = self.cuadruplos[Falso][0]
        goto_cond = self.cuadruplos[Falso][1]
        goto_return = len(self.cuadruplos)

        self.cuadruplos[Falso] = (goto_command, goto_cond, goto_return)

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
