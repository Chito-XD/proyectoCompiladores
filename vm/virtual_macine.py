

from utils.stack import Stack

from utils.types import get_type_from_address, get_cte_variable

from utils.constants import (
    OPER_LOG,
    ALL_OPERATIONS,
    LECTURA,
    ESCRIBE,
    GOTO,
    GOTO_F,
    GOTO_V,
    GLOBAL_SPACE_ADDRESS,
    LOCAL_SPACE_ADDRESS,
    CTE_SPACE_ADDRESS
)

class VirtualMachine:

    def __init__(self, cuad, dirr):
        self.cuadruplos = cuad
        self.directory = dirr
        self.memoryStack = Stack()

        self.print_directory()
    

    def run_cuadruplos(self):
        pointer = 0
        while( pointer < len(self.cuadruplos)):
            current_cuadruplo = self.cuadruplos[pointer]
            print(pointer, current_cuadruplo)

            operation = current_cuadruplo[0]
            if operation in ALL_OPERATIONS:
                op1 = current_cuadruplo[1]
                op2 = current_cuadruplo[2]
                result = self.evaluate_operation(op1, op2, operation)
                print("--> VM: OPERATION RESULT", result)
            
            elif operation == LECTURA:
                answer = input()
                # TODO: Esto debería de hacer, revisar la lectura en el manager, tiene que asignar la memoria y no la var
                # answer_type = get_cte_variable(answer)
                # memory_addres = get_type_from_address(current_cuadruplo[3])
                # if answer_type != memory_addres:
                #     raise Exception("==> INPUT MITMATCH", answer)
                print("--> VM : LECTURA: ", current_cuadruplo[3], answer)
            
            elif operation == ESCRIBE:
                print("--> VM : ESCRIBE: ", current_cuadruplo[3])
                # TODO: Dejar sólo el print
                # print(current_cuadruplo[3])

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