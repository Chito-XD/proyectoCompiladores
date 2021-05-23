

class MemoryStack:

    def __init__(self, dirr, cte_memory):
        
        self.directory = dirr
        self.cte_memory = cte_memory
        self.global_memory = {}
        self.memory_stack = []
        self.memory_pointer = -1

        self.arrange_cte_memory()
    
    def arrange_cte_memory(self):
        new_cte = {}
        for key in self.cte_memory.keys():
            new_cte[self.cte_memory[key]] = key
        self.cte_memory = new_cte
        
        print("")
        print("== > CTE MEMORY")
        print(self.cte_memory)
        print("")
    
    def pop_memory_stack(self):
        del self.memory_stack[-1]
        self.memory_pointer -= 1
    
    def push_memory_stack(self, clas, function, params=[]):
        main_process = self.directory.directory[clas]["proceso_global"]

        global_method_vars = self.directory.get_dir_variables(clas, main_process)
        current_method_vars = self.directory.get_dir_variables(clas, function)

        if len(params) > 0:
            for (index, var) in enumerate(current_method_vars):
                if index < len(params):
                    current_method_vars[var]["valor"] = params[index]
                    continue
                break
        
        memory = {}

        for key in current_method_vars.keys():
            var_dir = current_method_vars[key]["direccion"]
            memory[var_dir] = current_method_vars[key]["valor"]
        
        for key in global_method_vars.keys():
            var_dir = global_method_vars[key]["direccion"]
            if not self.global_memory.get(var_dir):
                self.global_memory[var_dir] = global_method_vars[key]["valor"]

        self.memory_stack.append(memory)
        self.memory_pointer += 1

    def get_value_from_address(self, address):
        if self.cte_memory.get(address):
            return self.cte_memory.get(address)
        elif self.memory_stack[self.memory_pointer].get(address):
            return self.memory_stack[self.memory_pointer][address]
        elif self.global_memory.get(address):
            return self.global_memory[address]
        
        self.memory_stack[self.memory_pointer][address] = None
        return None
    
    def assign_value_from_addresses(self, origin_add, target_add):
        value = self.get_value_from_address(origin_add)
        if self.memory_stack[self.memory_pointer].get(target_add):
            self.memory_stack[self.memory_pointer][target_add] = value
        else:
            self.global_memory[target_add] = value

    def set_value_from_address(self, address, value):
        if self.memory_stack[self.memory_pointer].get(address):
            self.memory_stack[self.memory_pointer][address] = value
        else: 
            self.global_memory[address] = value

    def set_return(self, key, value):
        self.global_memory[key] = value