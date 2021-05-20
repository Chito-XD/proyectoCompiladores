
from lex import Lex
from yacc import Yacc
from vm.virtual_macine import VirtualMachine


lexer = Lex()
parser = Yacc()

path = input()
data = open(path, 'r')

text = ""

for row in data:
    try:
        text = text + row.strip()
    except EOFError:
        break
    
if text: 
    # for tok in lexer.tokenize(text):
    #     print('type=%r, value=%r' % (tok.type, tok.value))
    if parser.parse(lexer.tokenize(text)):
        print('Correct syntaxis')

        cuadruplos = parser.manager.cuadruplos
        directory = parser.manager.directory

        vm = VirtualMachine(cuadruplos, directory)
        vm.run_cuadruplos()

    else:
        print('Incorrect syntaxis')