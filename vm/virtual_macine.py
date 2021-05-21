

from re import S
from utils.stack import Stack

from utils.types import get_type_from_address, get_cte_variable

from utils.constants import (
    OPER_LOG,
    ALL_OPERATIONS,
    LECTURA,
    ESCRIBE,
    ASSIGN,
    GOTO,
    GOTO_F,
    GOTO_V,
    GLOBAL_SPACE_ADDRESS,
    LOCAL_SPACE_ADDRESS,
    CTE_SPACE_ADDRESS
)

class VirtualMachine:

    def __init__(self, cuad, dirr, cte_memory):
        self.cuadruplos = cuad
        self.directory = dirr

        self.cte_memory = cte_memory

        self.memoryStack = []
        self.memory_pointer = 0

        self.class_name = "Main"
        self.function_name = "PRINCIAPAL"

        self.arrange_cte_memory()

        self.print_directory()
    
    def arrange_cte_memory(self):
        new_cte = {}
        for key in self.cte_memory.keys():
            new_cte[self.cte_memory[key]] = key
        self.cte_memory = new_cte
        
        print("")
        print("== > CTE MEMORY")
        print(self.cte_memory)
        print("")
    
    def push_memory_stack(self, clas, function):
        main_process = self.directory.directory[clas]["proceso_global"]

        global_method_vars = self.directory.get_dir_variables(clas, main_process)
        current_method_vars = self.directory.get_dir_variables(clas, function)

        memory = {}
        
        for key in global_method_vars.keys():
            var_dir = global_method_vars[key]["direccion"]
            memory[var_dir] = None
        
        for key in current_method_vars.keys():
            var_dir = current_method_vars[key]["direccion"]
            memory[var_dir] = None
        self.memoryStack.append(memory)
        
    def get_value_from_address(self, address):
        if self.cte_memory.get(address):
            return self.cte_memory.get(address)
        elif self.memoryStack[self.memory_pointer].get(address):
            return self.memoryStack[self.memory_pointer][address]
        
        self.memoryStack[self.memory_pointer][address] = None
        return None
    
    def assign_value_from_addresses(self, origin_add, target_add):
        value = self.get_value_from_address(origin_add)
        self.memoryStack[self.memory_pointer][target_add] = value

    def set_value_from_address(self, address, value):
        self.memoryStack[self.memory_pointer][address] = value

    def execute(self):
        # GOTO MAIN
        main_pointer = self.cuadruplos[0][3]
        self.push_memory_stack(self.class_name, self.function_name)
        self.run_cuadruplos(main_pointer)
    
    def run_cuadruplos(self, pointer=0):
        while( pointer < len(self.cuadruplos)):
            current_cuadruplo = self.cuadruplos[pointer]
            print(pointer, current_cuadruplo)

            operation = current_cuadruplo[0]

            if operation == ASSIGN:
                self.assign_value_from_addresses(current_cuadruplo[1], current_cuadruplo[3])

            if operation in ALL_OPERATIONS:
                op1 = self.get_value_from_address(current_cuadruplo[1])
                op2 = self.get_value_from_address(current_cuadruplo[2])

                result = self.evaluate_operation(op1, op2, operation)
                self.set_value_from_address(current_cuadruplo[3], result)
                # print("--> VM: OPERATION RESULT", result)
            
            elif operation == LECTURA:
                answer = input()
                answer_type = get_cte_variable(answer)
                memory_addres = get_type_from_address(current_cuadruplo[3])
                if answer_type != memory_addres:
                    raise Exception("==> INPUT MITMATCH", answer)
                self.set_value_from_address(current_cuadruplo[3], answer)
            
            elif operation == ESCRIBE:
                print(self.get_value_from_address(current_cuadruplo[3]))

            # elif operation == GOTO:
            #     pointer = int(current_cuadruplo[3])
            #     print('?????????????????? GOTO ', self.cuadruplos[pointer])
            
            # elif operation == GOTO_F:
            #     # TODO: Obtener el valor
            #     condition = current_cuadruplo[1]
            #     if condition is False:
            #         pointer = int(current_cuadruplo[3])
            #     else:
            #         pointer += 1

            # elif GOTO_V: 
            #     # TODO: Obtener el valor
            #     condition = current_cuadruplo[1]
            #     if condition is True:
            #         pointer = int(current_cuadruplo[3])
            #     else:
            #         pointer += 1
            
            pointer += 1

    
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

    
    def print_directory(self):
        self.directory.print_directory()