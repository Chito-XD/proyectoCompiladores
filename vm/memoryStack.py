from utils.types import get_scope_from_address

class MemoryStack:

    def __init__(self, dirr, cte_memory):
        
        self.directory = dirr
        self.cte_memory = cte_memory
        self.global_memory = {}
        self.memory_stack = []
        self.memory_pointer = -1

        self.memory_limit = 100000

        self.arrange_cte_memory()
    
    # Metodo que actualiza el stack
    def update_memory_limit(self, size):
        self.memory_limit += size
        if self.memory_limit < 0:
            raise Exception("Stack overfloww!!!")
    
    # Organiza el directoria de cte
    # {1: 1001, 2: 1002} => {1001: 1, 1002: 2}
    def arrange_cte_memory(self):
        new_cte = {}
        for key in self.cte_memory.keys():
            new_cte[self.cte_memory[key]] = key
        self.cte_memory = new_cte
        
        self.update_memory_limit( -1 * len(self.cte_memory.keys()) )

        print("")
        print("== > CTE MEMORY")
        print(self.cte_memory)
        print("")
    
    # Mata la memoria actual y despierta la anterior
    def pop_memory_stack(self):
        len_last_stack = len( self.memory_stack[-1].keys() )
        self.update_memory_limit(len_last_stack)

        del self.memory_stack[-1]
        self.memory_pointer -= 1
    
    # Duerme la memoria actual y crea otra
    def push_memory_stack(self, clas, function, params=[]):
        main_process = self.directory.directory[clas]["proceso_global"]

        global_method_vars = self.directory.get_dir_variables(clas, main_process)
        current_method_vars = self.directory.get_dir_variables(clas, function)

        # Guardar las variables que recibe un metodo como parámetro
        if len(params) > 0:
            for (index, var) in enumerate(current_method_vars):
                if index < len(params):
                    current_method_vars[var]["valor"] = params[index]
                    continue
                break
        
        memory = {}

        # Guardar variables en el stack
        for key in current_method_vars.keys():
            var_dir = current_method_vars[key]["direccion"]
            memory[var_dir] = current_method_vars[key]["valor"]
        
        self.update_memory_limit(-1 * len(memory.keys()) )
        
        # Guardar variables en el entorno global
        for key in global_method_vars.keys():
            var_dir = global_method_vars[key]["direccion"]
            if not self.global_memory.get(var_dir):
                self.global_memory[var_dir] = global_method_vars[key]["valor"]
                self.update_memory_limit(-1)

        self.memory_stack.append(memory)
        self.memory_pointer += 1

    # Obtener el valor real por medio de la dirección de memoria
    def get_value_from_address(self, address):
        if self.cte_memory.get(address) != None:
            return self.cte_memory.get(address)
        elif self.memory_stack[self.memory_pointer].get(address) != None:
            return self.memory_stack[self.memory_pointer][address]
        elif self.global_memory.get(address) != None:
            return self.global_memory[address]
        
        return None
    
    # asignar el valor de la dirrecion origin a la direcciónn objetivo
    def assign_value_from_addresses(self, origin_add, target_add):
        value = self.get_value_from_address(origin_add)
        self.set_value_from_address(target_add, value)

    # Asignar el valor dado a la dirreción con base en el scope de la direccion
    def set_value_from_address(self, address, value):
        if isinstance(address, str):
            if address.find('(') != -1:
                Aux = address.replace('(', '')
                Aux = Aux.replace(')', '')
                Aux = int(Aux)

        else:
            Aux = address

        scope = get_scope_from_address(Aux)
        if scope == "LOCAL":
            self.memory_stack[self.memory_pointer][address] = value
        else:
            self.global_memory[address] = value
        
        self.update_memory_limit(-1)

    # "Parche guadalupano" para setear el resultado a la variable global
    def set_return(self, key, value):
        if not self.global_memory.get(key):
            self.update_memory_limit(-1)
        self.global_memory[key] = value
    
    def print_memory(self):
        print('--------------')
        print('STACK')
        print(self.memory_stack)
        print('GLOBAL')
        print(self.global_memory)
        print('--------------')