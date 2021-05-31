# from os import replace
from typing import List
from vm.memoryStack import MemoryStack

from utils.types import get_type_from_address, get_cte_variable

from utils.constants import (
    OPER_LOG,
    ALL_OPERATIONS,
    LECTURA,
    ESCRIBE,
    ASSIGN,
    VERIFICA,
    GOTO,
    GOTO_F,
    ERA,
    REGRESA,
    PARAM,
    GOSUB,
    END_FUNCTION,
    PRINCIPAL,
    MAIN
)

class VirtualMachine:

    def __init__(self, cuad : List[tuple], dirr: dir, cte_memory: dir):
        self.cuadruplos = cuad
        self.directory = dirr

        self.memory = MemoryStack(dirr, cte_memory)

    # metodo para iniciar la ejecución de los cuadruplo
    def execute(self) -> None:
        # GOTO MAIN
        main_pointer = self.cuadruplos[0][3]
        # añada al stack de memoria
        self.memory.push_memory_stack(MAIN, PRINCIPAL)
        self.run_cuadruplos(main_pointer)
    
    # metodo para leer la direccion de memoria dependiente si es dir-base, apuntador o dirección normal
    def get_address_format(self, address_pointer: str) -> int:
        if isinstance(address_pointer, str):
            # direccion base
            if "dir-" in address_pointer:
                address_pointer = address_pointer.replace('dir-', '')
                return int(address_pointer)

            # apuntador de memoria
            if address_pointer[0] == "(" and address_pointer[-1] == ")":
                temp = self.memory.get_value_from_address(address_pointer)
                if temp != None:
                    return temp

                address_pointer = address_pointer.replace('(', '').replace(')', '')
                address_pointer = int(address_pointer)
                address = self.memory.get_value_from_address(address_pointer)
                return address
        
        # dirección de memoria
        return address_pointer
    
    # corre los cuadruplos
    def run_cuadruplos(self, pointer=0):

        while pointer < len(self.cuadruplos):
            # obtiene el cuadruplo en cuestion 
            current_cuadruplo = self.cuadruplos[pointer]
            # obtiene la operacion del cuadruplo
            operation = current_cuadruplo[0]

            # print(pointer, current_cuadruplo)

            # asinacion
            if operation == ASSIGN:
                operando1 = current_cuadruplo[1]
                operando3 = current_cuadruplo[3]

                add1 = self.get_address_format(operando1)
                add3 = self.get_address_format(operando3)

                self.memory.assign_value_from_addresses(origin_add=add1, target_add=add3)
                pointer += 1

            # operaciones aritmeticas
            elif operation in ALL_OPERATIONS:
                Operando1 = current_cuadruplo[1]
                Operando2 = current_cuadruplo[2]

                # revisa si es direccion de memoria. Si sí, suma el offset
                if isinstance(Operando1, str) and Operando1.find('dir-') != -1:
                    dirBase = Operando1.replace('dir-', '')
                    dirBase = int(dirBase)
                    op2 = self.memory.get_value_from_address(Operando2)
                    if op2 == None:
                        raise Exception("Variable no incializada")

                    result = self.evaluate_operation(dirBase, op2, operation)
                    self.memory.set_value_from_address(current_cuadruplo[3], result)
                
                # sino, obtener el valor de la direccion y ejecutar la operacion
                else:
                    add1 = self.get_address_format(Operando1)
                    add2 = self.get_address_format(Operando2)

                    op1 = self.memory.get_value_from_address(add1)
                    op2 = self.memory.get_value_from_address(add2)

                    if op1 == None or op2 == None:
                        raise Exception("Variable no incializada")
                    
                    result = self.evaluate_operation(op1, op2, operation)
                    self.memory.set_value_from_address(current_cuadruplo[3], result)
                
                pointer += 1
            
            # operacion de lectura
            elif operation == LECTURA:
                answer = input()
                answer_type = get_cte_variable(answer)

                memory_addres = current_cuadruplo[3]

                memory_type = get_type_from_address(memory_addres)
                if answer_type != memory_type:
                    raise Exception("==> INPUT MITMATCH", answer)

                self.memory.set_value_from_address(int(memory_addres), answer)
                pointer += 1
            
            # operacion de escritura
            elif operation == ESCRIBE:
                address = self.get_address_format(current_cuadruplo[3])
                value = self.memory.get_value_from_address(address)
                print(value)
                pointer += 1

            # cuadruplo de GOTO
            elif operation == GOTO:
                pointer = int(current_cuadruplo[2])

            # cuadruplo de goto_f
            elif operation == GOTO_F:
                condition = self.memory.get_value_from_address(current_cuadruplo[1])

                if condition == None:
                    raise Exception("No inicializada")

                # si la condicion se cumple, moverse al cuadruplo
                if not condition:
                    pointer = int(current_cuadruplo[2])
                else:
                    # sino, seguir al siguiente cuadruplo
                    pointer += 1

            # cuadruplo de verifica
            elif operation == VERIFICA:
                valor = int(self.memory.get_value_from_address(current_cuadruplo[1]))
                lim_inf = int(self.memory.get_value_from_address(current_cuadruplo[2]))
                lim_sup = int(self.memory.get_value_from_address(current_cuadruplo[3])) - 1

                if valor < lim_inf or valor > lim_sup:
                    raise Exception (f"{valor} is out of bounds of {lim_inf} and {lim_sup}")

                pointer += 1
            
            # cuadruplo de regres
            elif operation == REGRESA:
                address = current_cuadruplo[1]
                value = self.memory.get_value_from_address(current_cuadruplo[3])
                self.memory.set_return(address, value)
                return pointer

            # cuadruplo de era
            elif operation == ERA:
                # dejar la "migaja de pan" para sólo correr los cuadruplos del método que se llamo
                pointer = self.run_method(current_cuadruplo, pointer+1)

            # regresa al era
            elif operation == GOSUB:
                return pointer
            
            # regresa al era
            elif operation == END_FUNCTION:
                return pointer
            
            # regresa al era
            elif operation == PARAM:
                return pointer


    # metodo que ejecuta la logica del la llamada de los métodos
    # es específicamente para las llamadas, no para la declaración de los métodos
    def run_method(self, current_cuadruplo: tuple, pointer: int) -> int:

        current_pointer = pointer
        param_values = []

        # Primero revisamos los params, ejecutamos las operacion
        # hasta el momento en que encontramos el gosub
        while self.cuadruplos[current_pointer][0] != GOSUB:
            if self.cuadruplos[current_pointer][0] == PARAM:
                address = self.get_address_format(self.cuadruplos[current_pointer][1])
                value = self.memory.get_value_from_address(address)
                param_values.append(value)
                current_pointer += 1
            else:
                current_pointer = self.run_cuadruplos(current_pointer)
            
        function_name = current_cuadruplo[3]
        class_name = MAIN

        if "-" in function_name:
            class_name, function_name = function_name.split("-")

        # Una vez que ejecutamos todos los params, ahora sí, movemos el pointer
        # al inicio de la función
        pointer = self.directory.get_inicio(class_name, function_name)

        # creamos nuevo stack de memoria
        self.memory.push_memory_stack(class_name, function_name, param_values)

        # corremos los cuadruplos del método
        self.run_cuadruplos(pointer)

        # Logica del gosub
        # Remueve del stack la memoria local
        self.memory.pop_memory_stack()
        
        current_pointer += 1
        return current_pointer
        
    # metodo para ejecutar la operacion aritmetica
    def evaluate_operation(self, op1: str, op2: str, operator:str) -> str:
        if operator in OPER_LOG:
            if operator == '&':
                return (op1 and op2)
            else:
                return (op1 or op2)
        else:
            if operator == '<>':
                operator = '!='
            return eval( str(op1) + str(operator) + str(op2) )
