from functionDirectory import FunctionDirectory
from utils.constants import (
    PROCESO, 
    PRINCIPAL, 
    OPER_ARIT_PRIM, 
    OPER_ARIT_SEC, 
    ERROR,
    OPER_LOG,
    OPER_REL
)
from utils.queue import Queue
from utils.stack import Stack
from utils.types import get_type_operation, evaluate_operation

class ManagerSemantic():

    def __init__(self):
        self.directory = FunctionDirectory()
        self.currentType = None
        self.currentId = None
        self.currentVariables = Queue() # FI FO

        # Variables para cuadruplos
        self.operadores = Stack() #LI FO
        self.operandos = Stack()
        self.tipos = Stack()
        self.saltos = Stack()
        
        # Cuadruplos
        self.cuadruplos = []

    
    def set_current_type(self, var_type):
        self.currentType = var_type
    
    def set_current_id(self, curr_id):
        self.currentId = curr_id
    
    def delete_current_type(self):
        self.currentType = None
    
    def delete_currentId(self):
        self.currentId = None

    def create_function_directory(self, program_id):
        params = {
            "tipo": PROCESO
        }
        self.directory.createFunction(program_id, params)
    
    def add_function(self, program_id):
        params = {
            "tipo": self.currentType
        }
        self.directory.createFunction(program_id, params)
    
    def create_principal(self, program_id):
        params = {
            "tipo": PRINCIPAL
        }
        self.directory.createFunction(program_id, params)
    
    def stash_variable(self, var):
        self.currentVariables.add(var)
    
    def store_variables(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.pop()
            params = {
                "key": var,
                "tipo": self.currentType
                # "value": 
            }
            self.directory.addLocalVariable(self.currentId, params)
        self.deleteCurrentType()
    
    def update_variable(self, var, value):
        params = {
            "key": var,
            "value": value
        }
        self.directory.updateVariable(self.currentId, params)

    def insert_operando_type(self, operando, type_o):
        self.operandos.push(operando)
        self.tipos.push(type_o) #revisar 
    
    def insert_operador(self, operador):
        self.operadores.push(operador)

    def create_cruadruplo(self, operator, op_izq, op_der, temporal):
        self.cuadruplos.append((operator, op_izq, op_der, temporal))

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
            result = evaluate_operation(op_izq, op_der, op)
            self.create_cruadruplo(op, op_izq, op_der, result)
            self.create_cruadruplo(op, tipo_izq, tipo_der, operation_type) # Revisar esto
        else:
            raise Exception(f"No se puede evaluar -> {op_izq} {op} {op_der}")

    def create_asignacion(self):
        res = self.operandos.pop()
        tipo_resultado = self.tipos.pop()
        lado_izq = self.operadores.pop()
        tipo_izq = self.tipos.pop()

        operator_type = get_type_operation(tipo_resultado, tipo_izq, '=')
        if operator_type is not ERROR:
            self.create_cruadruplo("=", res, None, lado_izq)

    def create_escritura(self, variable):
        self.create_cruadruplo("ESCRIBE", None, None, variable)
    
    def create_lectura(self, op):
        # Validar que la var exista
        variables = self.directory[self.currentId]["directorio_variables"]
        variable = variables.get(op, None)
        if variable: 
            # Si existe la variable, entonces, creas el cuadruplo de lectura
            self.create_cruadruplo("LECTURA", None, None, op)
        else:
            raise Exception("La variable que se quiere leer no existe")
    
    