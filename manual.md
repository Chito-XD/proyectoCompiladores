# Manual de usuario

Para iniciar a codificar en este lenguaje, es de suma importancia declarar el nombre del programa y una función principal. El programa empieza a correr desde la primera línea de la función principal:
```
programa nombrePrograma;

principal(){

}
````

# Variables globales

Para declarar las variables, tiene que ser antes de la función principal. Para ello, es necesario poner explícitamente la palabara **variables:** y a partir de ahí, escribir las variables del programa. 

Los tipos simples permitidos son: **entero, flotante, booleano** y **char**.

Siguiendo con el ejemplo de arriba al declarar algunas variables, quedaría de la siguiente mannera:
```
programa nombrePrograma;

variables:
    f: flotante;
    a, b: entero;
    cadena: char;
    bool: booleano;

principal(){

}
```

# Metodos

Para declarar métodos, es estricticamente necesario tres aspectos:
- valor de retorno: tipo que regresa la función.
- nombre de la función: identificador único a lo largo del programa. 
- parámetros: variables de tipo simple declaradas una por una. En caso de no recibir alguna variable, dejar vacío).

Siguiendo con el ejemplo anterior, el programa quedaría de la siguiente manera:
```
programa nombrePrograma;

variables:
    f: flotante;
    a, b: entero;
    cadena: char;
    bool: booleano;

entero funcion multiplica(x: entero, y: entero)
{

}

principal(){

}
```

# Variables  locales
Si bien tenemos variables globales que pueden ser modificados a lo largo del programa, es posible declarar variables de scope local dentro de los métodos previamente declarados. Inclusive, estas variables pueden tener el mismo nombre que una variable global y el programa sabrá diferenciar cada una.

Siguiendo con el ejemplo anterior, el programa quedaría de la siguiente manera:
```
programa nombrePrograma;

variables:
    f: flotante;
    a, b: entero;
    cadena: char;
    bool: booleano;

entero funcion multiplica(x: entero, y: entero)
variables: 
    a: entero;
    resultado: entero;
{

}

principal(){

}
```


# Llamadas a funciones

Una vez declarada una función, es posible llamarla desde cualquier otro método o de la función principal. Para ello, es importante conocer si el método tiene algún tipo de valor de retorno o es una función void.
De igual maenra, saber si recibe parámetros y de qué tipo.

Siguiendo con el ejemplo anterior, el programa quedaría de la siguiente manera:
```
programa nombrePrograma;

variables:
    f: flotante;
    a, b: entero;
    cadena: char;
    bool: booleano;

entero funcion multiplica(x: entero, y: entero)
variables: 
    a: entero;
    resultado: entero;
{

}

principal(){
    a = mutiplica(2, 5);
}
```






# Operaciones

El lenguaje soporta las operaciones aritméticas, lógicas y relacionales básicas con la jerarquía tradicional.

De tal manera, es posible realizar una operación y asignar el resultado a un valor.

En caso de querer interactura con el usuario. Es posible solicitar e imprimir ciertos resultados por medio de las siguientes funciones: 
- lee();

Permite obtener el valor del usuario por medio de la línea de comandos y asingar a la variable en cuestión. 
- escribe();

Permite escribir el resultado final de una variable o de una función. 

Siguiendo con el ejemplo anterior, el programa quedaría de la siguiente manera:
```
programa nombrePrograma;

variables:
    f: flotante;
    a, b: entero;
    final: entero;
    cadena: char;
    bool: booleano;

entero funcion multiplica(x: entero, y: entero)
variables: 
    a: entero;
    resultado: entero;
{
    a = x * y + 7;
    resultado = a;
    regresa(resultado);

}

principal(){
    lee(a);
    lee(b);
    final = mutiplica(a, b);
    escribe("El resultado es"; final);
}
```

# Ciclos 

Para realizar algún tipo de ciclo o flujos no lineales, hay dos posibilidades de realizarlo. 

- Mientras:
     
    Con esta sintaxis, el código ejecutará el código siempre y cuando la condición se siga cumplinedo. La sintaxis quedaría de la siguiente manera: 
    ```
    mientras (x < 10 ) hacer {
        ...
        x = x + 1;
    }
    ```

- Desde
    
    El *desde* funciona de manera muy similar al *mientras* aunque el contador del ciclo va aumentando de uno en uno de manera natural. La sintaxis quedaría de la siguiente manera:
    ```
    dede x = 1 hasta 10 hacer {
        ...
    }
    ```


# Decisiones

Estos estructuras nos permiten a correr ciertos pedazos de código dependiendo de la condición que se quiera evaluar. Las sintaxis queda de la siguiente manera:

```
si (x == 1) entonces {
    ...
}
...
```
También es posible poner una sección en caso de que la condición no se cumpla:

```
si (x == 1) entonces {
    ...
} sino {
    ...
}
...
```



# Objetos
El lenguaje permite programar en objetos. Los objetos tienen la misma sintaxis y lógica de las estructuras anteriores. El beneficio de crear algun objeto es crear otro scope y almacenas distinta información. 

Siguiendo con el ejemplo del principio y la nueva sintaxis, quería de la siguiente manera: 

```
programa nombrePrograma;
Clase Calculo {
    atributos:
        f: flotante;
        e: entero;
    
    metodos:
        entero funcion uno(a: entero, b: entero)
        variables:
            c : entero;
        {
            c = a * b;
            regresa(c);
        }
}

variables:
    f: flotante;
    a, b: entero;
    final: entero;
    cadena: char;
    bool: booleano;
    cal: Calculo;

entero funcion multiplica(x: entero, y: entero)
variables: 
    a: entero;
    resultado: entero;
{
    a = x * y + 7;
    resultado = a;
    regresa(resultado);

}

principal(){
    lee(a);
    lee(b);
    final = mutiplica(a, b);
    escribe("El resultado es"; final);
    escribe(cal.uno(3, 9));
}
```