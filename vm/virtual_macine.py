from os import replace
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
    END_FUNCTION
)

class VirtualMachine:

    def __init__(self, cuad, dirr, cte_memory):
        self.cuadruplos = cuad
        self.directory = dirr

        self.memory = MemoryStack(dirr, cte_memory)

        self.class_name = "Main"
        self.function_name = "PRINCIAPAL"

        self.directory.print_directory()

        a = 0
        for i in cuad:
            print(a, i)
            a += 1
        print("")
    
    def execute(self):
        # GOTO MAIN
        main_pointer = self.cuadruplos[0][3]
        self.memory.push_memory_stack(self.class_name, self.function_name)
        self.run_cuadruplos(main_pointer)
    
    def get_address_format(self, address_pointer):
        if isinstance(address_pointer, str):

            if "dir-" in address_pointer:
                address_pointer = address_pointer.replace('dir-', '')
                return int(address_pointer)

            if address_pointer[0] == "(" and address_pointer[-1] == ")":
                temp = self.memory.get_value_from_address(address_pointer)
                if temp != None:
                    return temp

                address_pointer = address_pointer.replace('(', '').replace(')', '')
                address_pointer = int(address_pointer)
                address = self.memory.get_value_from_address(address_pointer)
                return address
        return address_pointer
    
    def run_cuadruplos(self, pointer=0):

        while pointer < len(self.cuadruplos):

            current_cuadruplo = self.cuadruplos[pointer]
            operation = current_cuadruplo[0]

            print(pointer, current_cuadruplo)

            if operation == ASSIGN:
                operando1 = current_cuadruplo[1]
                operando3 = current_cuadruplo[3]

                add1 = self.get_address_format(operando1)
                add3 = self.get_address_format(operando3)


                # print(operando1, operando3, add1, add3)

                self.memory.assign_value_from_addresses(origin_add=add1, target_add=add3)
                pointer += 1
                # print(self.memory.memory_stack)
                # print(self.memory.global_memory)

            elif operation in ALL_OPERATIONS:
                Operando1 = current_cuadruplo[1]
                Operando2 = current_cuadruplo[2]

                if isinstance(Operando1, str) and Operando1.find('dir-') != 1:
                    dirBase = Operando1.replace('dir-', '')
                    # print("DirBase:",dirBase)
                    dirBase = int(dirBase)
                    op2 = self.memory.get_value_from_address(Operando2)
                    if op2 == None:
                        raise Exception("Variable no incializada")

                    result = self.evaluate_operation(dirBase, op2, operation)
                    # print("Resultado:", result)
                    self.memory.set_value_from_address(current_cuadruplo[3], result)
                
                else:
                    add1 = self.get_address_format(Operando1)
                    add2 = self.get_address_format(Operando2)

                    op1 = self.memory.get_value_from_address(add1)
                    op2 = self.memory.get_value_from_address(add2)

                    # print(add1, add2, op1, op2)

                    if op1 == None or op2 == None:
                        raise Exception("Variable no incializada")
                    
                    result = self.evaluate_operation(op1, op2, operation)
                    self.memory.set_value_from_address(current_cuadruplo[3], result)
                
                # print(self.memory.memory_stack)
                # print(self.memory.global_memory)
                pointer += 1
            
            elif operation == LECTURA:
                answer = input()
                answer_type = get_cte_variable(answer)

                memory_addres = self.memory.get_value_from_address(current_cuadruplo[3])

                # print("memory addres", memory_addres)
                
                memory_type = get_type_from_address(memory_addres)
                if answer_type != memory_type:
                    raise Exception("==> INPUT MITMATCH", answer)
                # print("ey", current_cuadruplo[3], answer, memory_addres)


                self.memory.set_value_from_address(int(memory_addres), answer)
                pointer += 1
                # print(self.memory.memory_stack)
                # print(self.memory.global_memory)
            
            elif operation == ESCRIBE:
                address = self.get_address_format(current_cuadruplo[3])
                value = self.memory.get_value_from_address(address)
                # print(address)
                print(value)
                pointer += 1

            elif operation == GOTO:
                pointer = int(current_cuadruplo[2])

            elif operation == GOTO_F:
                condition = self.memory.get_value_from_address(current_cuadruplo[1])

                if condition == None:
                    raise Exception("No inicializada")

                if not condition:
                    pointer = int(current_cuadruplo[2])
                else:
                    pointer += 1

            elif operation == VERIFICA:
                valor = int(self.memory.get_value_from_address(current_cuadruplo[1]))
                lim_inf = int(self.memory.get_value_from_address(current_cuadruplo[2]))
                lim_sup = int(self.memory.get_value_from_address(current_cuadruplo[3])) - 1

                # print(valor, lim_inf, lim_sup)

                if valor < lim_inf or valor > lim_sup:
                    raise Exception (f"{valor} is out of bounds of {lim_inf} and {lim_sup}")

                pointer += 1
            
            elif operation == REGRESA:
                address = current_cuadruplo[1]
                value = self.memory.get_value_from_address(current_cuadruplo[3])
                self.memory.set_return(address, value)
                # print(self.memory.memory_stack)
                # print(self.memory.global_memory)
                return pointer

            elif operation == ERA:
                pointer = self.run_method(current_cuadruplo, pointer+1)

            elif operation == GOSUB:
                return pointer
            
            elif operation == END_FUNCTION:
                return pointer
            
            elif operation == PARAM:
                return pointer


    # metodo que ejecuta la logica del la llamada de los métodos
    # es específicamente para las llamadas, no para la declaración de los métodos
    def run_method(self, current_cuadruplo, pointer):

        current_pointer = pointer
        param_values = []

        # Primero revisamos los params, ejecutamos las operacion
        # hasta el momento en que encontramos el gosub
        while self.cuadruplos[current_pointer][0] != GOSUB:
            if self.cuadruplos[current_pointer][0] == PARAM:
                address = self.get_address_format(self.cuadruplos[current_pointer][1])
                value = self.memory.get_value_from_address(address)
                print("PARAM VALUE", value)
                param_values.append(value)
                current_pointer += 1
            else:
                current_pointer = self.run_cuadruplos(current_pointer)
            
        # Una vez que ejecutamos todos los params, ahora sí, movemos el pointer
        # al inicio de la función
        self.function_name = current_cuadruplo[3]
        pointer = self.directory.get_inicio(self.class_name, self.function_name)

        # creamos nuevo stack de memoria
        self.memory.push_memory_stack(self.class_name, self.function_name, param_values)

        # corremos los cuadruplos del método
        self.run_cuadruplos(pointer)

        # TODO: Logica del gosub
        self.memory.pop_memory_stack()
        

        current_pointer += 1
        return current_pointer
        

    def evaluate_operation(self, op1, op2, operator):
        if operator in OPER_LOG:
            if operator == '&':
                return (op1 and op2)
            else:
                return (op1 or op2)
        else:
            if operator == '<>':
                operator = '!='
            return eval( str(op1) + str(operator) + str(op2) )
