from functionDirectory import FunctionDirectory
from utils.constansts import (PROCESO, PRINCIPAL, OPER_ARIT_PRIM, OPER_ARIT_SEC, ERROR)
from utils.queue import Queue
from utils.stack import Stack
from utils.types import get_type_from_operator, get_value_from_operator

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
        self.tipos.push(type_o)
    
    def insert_operador(self, operador):
        self.operadores.push(operador)
    
    def create_cruadruplo(self, ope_izq, ope_der, operator):

        # Revisar la lógica de cuando el operador derecho está vacío

        # Validar si la operacion entre los dos es válida
        operator_type = get_type_from_operator(ope_izq, ope_der, operator)
        if operator_type is not ERROR:
            result = get_value_from_operator(ope_izq, ope_der, operator)
            self.cuadruplos.append((operator, ope_izq, ope_der, result))
        else:
            raise Exception("No es posible hacer la operación")
    

    # REVISAR METODO
    def creat_asignacion(self, op):
        self.cuadruplos.append(("=", None, None, op))

    def crear_escritura(self, op):
        self.cuadruplos.append(("ESCRIBE", None, None, op))
    
    def creat_lectura(self, op):
        # Validar que la var exista
        variables = self.directory[self.currentId]["directorio_variables"]
        variable = variables.get(op, None)
        if variable: 
            # Si existe la variable, entonces, creas el cuadruplo de lectura
            self.cuadruplos.append(("LECTURA", None, None, op))
        else:
            raise Exception("La variable que se quiere leer no existe")
    
    