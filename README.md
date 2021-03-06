# Lenguaje Team ++

Team 5 
Integrantes: 
- Néstor Martínez A00819796
- Edgar Rubén Salazar Lugo A01338798


# Link Github
https://github.com/Chito-XD/proyectoCompiladores

# Link al manual
https://github.com/Chito-XD/proyectoCompiladores/blob/main/manual.md

# Link al video demo
https://youtu.be/VtTWrzjSPu0

# Link a la documentacion final del proyecto
https://docs.google.com/document/d/138oFLWWfGP6kZ9k_BCYM1gZxiAHZcxY2Kp5HNKSER_o/edit?usp=sharing

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

## Avance 3: Generación de código intermedio inicial
- Adición de lógica para cuadruplos aritméticos, lógicos y relacionales
- Adición de lógica para cuadruplos de escritura, lectura y avance de asignación.
- Validación de operaciones entre tipos.


*Pendientes*
- Integración de la sintaxis con el manager de semántica (Por el momento creamos la lógica por parte del manager, pero no lo hemos integrado a la semántica a pesar de tener ciertos puntos neuralgicos).
- Probar la correcta creación de los cuadruplos y puntos neuralgicos.


## Avance 4: Generación de código intermedio para estatutos no-lineales
- Integración completa de la sintaxis y semántica.
- Corrección del manager de la semántica
- Integración de cuadruplos de lectura, escritura y asignación
- Integración de código intermedio de if's, while y desde. 

*Pendientes*
- Corregir ligeros detalles del goto. 
- Realizar ajustes de sintaxis con base en la lógica de métodos y llamadas de clases

## Avance 5:
- Se corrigieron errores de los estatutos no lineales como por ejemplo que los saltos se creaban antes que los cuadruplos de las comparaciones
- Se corrigio que se crearon 2 versiones de los saltos
- Se corrigio que en la asignacion, no se hacia pop al operador de asignacion (=)
- Se corrigio la funcion para crear el cuadruplo de lectura
- Se modificó la sintaxis para poder recibir funciones, asignar funciones a variables y llamadas a propiedades de objetos.

*Pendientes*
- Cuadruplos de llamadas de funciones
- Asignación de variables a llamadas
- Escribir atributos de clases
- Revisar los cuadruplos -> orden
- return 
- Objetos 
- FOR loop
- Arreglar el 'enter' en declaración de variables
- DUDAS --> Funciones de clases

## Avance 6:
- Flujo de cruadruplos para funciones
- Cuadruplos para llamada de funciones
- Adición de lógica de memoria global, local y cte
- Fix de 'enter' en dec de variables


*Pendientes*
- Objetos 
- FOR loop
- return
- DUDAS --> Funciones de clases


## Avance 7 y 8:
- Se crearon los cuadruplos de arreglos
- Se ejecutan los arreglos y sus operaciones junto con su indexacion
- Se ejecutan las funciones de los objetos
*Pendientes*
- 1) Objetos - Atributos
- 2) Regresa resultado de función (creo que es flotante)
- 3) string - operaciones?
- 4) negativos
- 5) comentarios

- Documentación