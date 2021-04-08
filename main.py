
from lex import Lex
from yacc import Yacc


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
    if parser.parse(lexer.tokenize(text)):
        print('Correct syntaxis')
    else:
        print('Incorrect syntaxis')