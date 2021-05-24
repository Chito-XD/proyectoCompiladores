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
    
    def run_cuadruplos(self, pointer=0):

        while pointer < len(self.cuadruplos):

            current_cuadruplo = self.cuadruplos[pointer]
            operation = current_cuadruplo[0]

            print(pointer, current_cuadruplo)

            if operation == ASSIGN:
                self.memory.assign_value_from_addresses(current_cuadruplo[1], current_cuadruplo[3])
                pointer += 1

            elif operation in ALL_OPERATIONS:
                # TODO: Revisar si es direccion o voy por valor
                op1 = self.memory.get_value_from_address(current_cuadruplo[1])
                op2 = self.memory.get_value_from_address(current_cuadruplo[2])

                if not op1 or not op2:
                    raise Exception("Variable no inicializada")

                result = self.evaluate_operation(op1, op2, operation)
                self.memory.set_value_from_address(current_cuadruplo[3], result)
                pointer += 1
            
            elif operation == LECTURA:
                answer = input()
                answer_type = get_cte_variable(answer)
                memory_addres = get_type_from_address(current_cuadruplo[3])
                if answer_type != memory_addres:
                    raise Exception("==> INPUT MITMATCH", answer)
                self.memory.set_value_from_address(current_cuadruplo[3], answer)
                pointer += 1
            
            elif operation == ESCRIBE:
                print(self.memory.get_value_from_address(current_cuadruplo[3]))
                pointer += 1

            elif operation == GOTO:
                pointer = int(current_cuadruplo[2])

            elif operation == GOTO_F:
                condition = self.memory.get_value_from_address(current_cuadruplo[1])
                if not condition:
                    pointer = int(current_cuadruplo[2])
                else:
                    pointer += 1

            elif operation == VERIFICA:
                pointer += 1
            
            elif operation == REGRESA:
                address = current_cuadruplo[1]
                value = self.memory.get_value_from_address(current_cuadruplo[3])

                self.memory.set_return(address, value)

                # pointer += 1
                return pointer

            elif operation == ERA:
                pointer = self.run_method(current_cuadruplo, pointer+1)

            elif operation == GOSUB:
                return pointer
            
            elif operation == END_FUNCTION:
                return pointer
            
            elif operation == PARAM:
                return pointer

            # else: 
            #     pointer += 1
    

    def run_method(self, current_cuadruplo, pointer):

        current_pointer = pointer
        param_values = []

        while self.cuadruplos[current_pointer][0] != GOSUB:
            if self.cuadruplos[current_pointer][0] == PARAM:
                value = self.memory.get_value_from_address(self.cuadruplos[current_pointer][1])
                print("PARAM VALUE", value)
                param_values.append(value)
                current_pointer += 1
            else:
                current_pointer = self.run_cuadruplos(current_pointer)
            
        self.function_name = current_cuadruplo[3]
        pointer = self.directory.get_inicio(self.class_name, self.function_name)

        self.memory.push_memory_stack(self.class_name, self.function_name, param_values)

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
