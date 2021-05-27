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
                Operando1 = current_cuadruplo[1]
                Operando3 = current_cuadruplo[3]

                if isinstance(Operando1, str) :
                    if Operando1.find('(') != -1:
                        Aux = Operando1.replace('(', '')
                        Aux = Aux.replace(')', '')
                        Aux = int(Aux)
                        print("Aux:",Aux)
                        Dir = self.memory.get_value_from_address(Aux)
                        print("DireccionOp1:",Dir)
                        op1 = self.memory.get_value_from_address(Dir)
                        print("Op1:",op1)
                        if not op1:
                            raise Exception("Instancia del arreglo sin valor")
                        else:
                            self.memory.assign_value_from_addresses(Dir, current_cuadruplo[3])

                elif isinstance(Operando3, str):
                    if Operando3.find('(') != -1:
                        Aux = Operando3.replace('(', '')
                        Aux = Aux.replace(')', '')
                        Aux = int(Aux)
                        Dir = self.memory.get_value_from_address(Aux)
                        print("DireccionOp3:",Dir)
                        self.memory.assign_value_from_addresses(current_cuadruplo[1], Dir)

                    else:
                        self.memory.assign_value_from_addresses(current_cuadruplo[1], current_cuadruplo[3])
                else:
                    self.memory.assign_value_from_addresses(current_cuadruplo[1], current_cuadruplo[3])

                pointer += 1

            elif operation in ALL_OPERATIONS:
                # TODO: Revisar si es direccion o voy por valor 

                Operando1 = current_cuadruplo[1]
                Operando2 = current_cuadruplo[2]
                
                if isinstance(Operando1, str) | isinstance(Operando2,str):

                   if Operando1.find('dir-') != 1:
                        Aux = Operando1.replace('dir-', '')
                        print("DirBase:",Aux)
                        op1 = int(Aux)
                        op2 = self.memory.get_value_from_address(current_cuadruplo[2])
                        if not op2:
                            raise Exception("Variable no incializada")

                        result = self.evaluate_operation(op1, op2, operation)
                        print("Resultado:", result)
                        self.memory.set_value_from_address(current_cuadruplo[3], result)
                        print(self.memory.memory_stack)
                        pointer += 1


                   elif Operando1.find('('):
                        Aux = Operando1.replace('(', '')
                        Aux = Aux.replace(')', '')
                        Dir = self.memory.get_value_from_address(Aux)
                        op1 = self.memory.get_value_from_address(Dir)
                        op2 = self.memory.get_value_from_address(current_cuadruplo[2])

                        print("Direccion:", Dir)
                        print("Valor:", op1)

                        if not op1 or not op2:
                            raise Exception("Variable no incializada")

                        result = self.evaluate_operation(op1, op2, operation)
                        self.memory.set_value_from_address(current_cuadruplo[3], result)
                        pointer += 1

                   elif Operando2.find('('):
                        Aux = Operando2.replace('(', '')
                        Aux = Aux.replace(')', '')
                        Dir = self.memory.get_value_from_address(Aux)
                        op1 = self.memory.get_value_from_address(Dir)
                        op2 = self.memory.get_value_from_address(current_cuadruplo[2])

                        if not op1 or not op2:
                            raise Exception("Variable no incializada")

                        result = self.evaluate_operation(op1, op2, operation)
                        self.memory.set_value_from_address(current_cuadruplo[3], result)
                        pointer += 1

                        # raise Exception("Variable de direccion")
                   else:
                        op1 = self.memory.get_value_from_address(current_cuadruplo[1])
                        op2 = self.memory.get_value_from_address(current_cuadruplo[2])

                        if not op1 or not op2:
                            raise Exception("Variable no inicializada")

                        result = self.evaluate_operation(op1, op2, operation)
                        self.memory.set_value_from_address(current_cuadruplo[3], result)
                        pointer += 1
                    
                else:
                    op1 = self.memory.get_value_from_address(current_cuadruplo[1])
                    op2 = self.memory.get_value_from_address(current_cuadruplo[2])

                    if not op1 or not op2:
                        raise Exception("Variable no inicializada")

                    result = self.evaluate_operation(op1, op2, operation)
                    self.memory.set_value_from_address(current_cuadruplo[3], result)
                    pointer += 1

                if op1 == None or op2 == None:
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
                aux = current_cuadruplo[3]

                if isinstance(aux, str) and  aux[0] == "(" and aux[-1] == ")":
                    aux = aux.replace('(', '')
                    aux = aux.replace(')', '')
                    aux = int(aux)
                    address = self.memory.get_value_from_address(aux)
                    value = self.memory.get_value_from_address(address)
                    # print("AUXXXXX", aux, address, value)
                    print(value)
                else:
                    # print("AUXXXXX", aux)
                    print(self.memory.get_value_from_address(aux))
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
                Valor = int(self.memory.get_value_from_address(current_cuadruplo[1]))
                LimInf = int(self.memory.get_value_from_address(current_cuadruplo[2]))
                LimSup = int(self.memory.get_value_from_address(current_cuadruplo[3])) - 1

                print(Valor, LimInf, LimSup)

                if Valor < LimInf or Valor > LimSup:
                    raise Exception ("Out of bounds")

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
    

    # metodo que ejecuta la logica del la llamada de los métodos
    # es específicamente para las llamadas, no para la declaración de los métodos
    def run_method(self, current_cuadruplo, pointer):

        current_pointer = pointer
        param_values = []

        # Primero revisamos los params, ejecutamos las operacion
        # hasta el momento en que encontramos el gosub
        while self.cuadruplos[current_pointer][0] != GOSUB:
            if self.cuadruplos[current_pointer][0] == PARAM:
                value = self.memory.get_value_from_address(self.cuadruplos[current_pointer][1])
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
