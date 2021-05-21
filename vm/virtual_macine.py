

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
    ERA,
    GOSUB,
    END_FUNCTION
)

class VirtualMachine:

    def __init__(self, cuad, dirr, cte_memory):
        self.cuadruplos = cuad
        self.directory = dirr

        self.cte_memory = cte_memory

        self.memory_stack = []
        self.memory_pointer = -1

        self.class_name = "Main"
        self.function_name = "PRINCIAPAL"

        self.arrange_cte_memory()

        self.print_directory()
        a = 0
        for i in cuad:
            print(a, i)
            a += 1
        print("")
    
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

        self.memory_stack.append(memory)
        self.memory_pointer += 1

        # print("MEMORY_STACK")
        # print(self.memory_stack);
        
    def get_value_from_address(self, address):
        if self.cte_memory.get(address):
            return self.cte_memory.get(address)
        elif self.memory_stack[self.memory_pointer].get(address):
            return self.memory_stack[self.memory_pointer][address]
        
        self.memory_stack[self.memory_pointer][address] = None
        return None
    
    def assign_value_from_addresses(self, origin_add, target_add):
        value = self.get_value_from_address(origin_add)
        self.memory_stack[self.memory_pointer][target_add] = value

    def set_value_from_address(self, address, value):
        self.memory_stack[self.memory_pointer][address] = value

    def execute(self):
        # GOTO MAIN
        main_pointer = self.cuadruplos[0][3]
        self.push_memory_stack(self.class_name, self.function_name)
        self.run_cuadruplos(main_pointer)
    
    def run_cuadruplos(self, pointer=0):

        while( pointer < len(self.cuadruplos)):

            current_cuadruplo = self.cuadruplos[pointer]
            operation = current_cuadruplo[0]

            print(pointer, current_cuadruplo)

            if operation == ASSIGN:
                self.assign_value_from_addresses(current_cuadruplo[1], current_cuadruplo[3])
                pointer += 1

            if operation in ALL_OPERATIONS:
                op1 = self.get_value_from_address(current_cuadruplo[1])
                op2 = self.get_value_from_address(current_cuadruplo[2])

                result = self.evaluate_operation(op1, op2, operation)
                self.set_value_from_address(current_cuadruplo[3], result)
                pointer += 1
            
            elif operation == LECTURA:
                answer = input()
                answer_type = get_cte_variable(answer)
                memory_addres = get_type_from_address(current_cuadruplo[3])
                if answer_type != memory_addres:
                    raise Exception("==> INPUT MITMATCH", answer)
                self.set_value_from_address(current_cuadruplo[3], answer)
                pointer += 1
            
            elif operation == ESCRIBE:
                print(self.get_value_from_address(current_cuadruplo[3]))
                pointer += 1

            elif operation == GOTO:
                pointer = int(current_cuadruplo[2])

            elif operation == GOTO_F:
                condition = self.get_value_from_address(current_cuadruplo[1])
                if not condition:
                    pointer = int(current_cuadruplo[2])
                else:
                    pointer += 1

            elif operation == ERA:
                print("== ERA")
                self.function_name = current_cuadruplo[3]
                self.push_memory_stack(self.class_name, self.function_name)
                pointer = self.directory.get_inicio(self.class_name, self.function_name)
            
            elif operation == GOSUB:
                print("== GOSUB")
                pointer += 1
            
            elif operation == END_FUNCTION:
                print(" == END_FUNCTION")
                pointer = 100000

            # else: 
            #     pointer += 1
            

    
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