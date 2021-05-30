
from lex import Lex
from yacc import Yacc
from vm.virtual_macine import VirtualMachine


lexer = Lex()
parser = Yacc()

# lee el path del test a probar
path = input()
data = open(path, 'r')

text = ""

for row in data:
    try:
        text = text + row.strip()
    except EOFError:
        break
    
if text: 
    # corre el lexer y parser
    if parser.parse(lexer.tokenize(text)):
        cuadruplos = parser.manager.cuadruplos
        directory = parser.manager.directory
        cte_memory = parser.manager.memory.cte_vars
        
        # corre la maquina virtual
        vm = VirtualMachine(cuadruplos, directory, cte_memory)
        vm.execute()

    else:
        print('Incorrect syntaxis')