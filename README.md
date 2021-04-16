# Lenguaje Team ++

Team 5 
Integrantes: 
- Néstor Martínez A00819796
- Edgar Rubén Salazar Lugo A01338798

## Avance 1
- Lexer: Archivo que hace un listado de todos los tokens (lex.py)
- Parser: Archivo que analiza la sintáxis del lenguajes (yacc.py)
- Main: Archivo que lee de un archivo de texto el lenguaje y aplica el Lexer y Parser (main.py)
- Gramática: Archivo que contiene la información de la gramática libre de contexto del lenguaje (gramatica.txt).
- Test de lenguaje: Archivo de texto que contiene el lenguaje de prueba (test1.txt)

## Avance 2: Semántica básica
- Directorio de funciones: Clase para manejar toda la lógica relacionada al directorio de funciones. Cada función tiene una propiedad que apunta a su tabla de variables. (funcitonDirectory.py)
- Tabla de variables: Clase para manejar toda la lógica de la tabla de variables. A ser un atributo de cada función, no hay necesidad de identificar cada instancia. (tabVars.py)
- Manager: Clase que funciona como un manager entre la sintáxis y semántica. Este manager es la que interacturá directamente con la sintaxis. Como uno de sus atributos es el directorio de funciones. (managerSemantic.py)
- Type matching: Directorio que contiene la información de la tabla de tipos. Esta variable está dentro del archivo constants.py
- Tabla de consideraciones semánticas: Puntos donde marcamos los puntos en los que el Manager intervendría para manejar el directorio de funciones, tabla de variables, etc. 
- Queue y Stack: Adición de las clases de una cola y un stack (queue.py y stack.py)