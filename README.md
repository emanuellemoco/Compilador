#### Diagrama Sintático

[![Diagrama](https://i.imgur.com/UwtR865.jpeg)]()


#### EBNF


BLOCK = { COMMAND } ;
COMMAND = ( λ | ASSIGNMENT | PRINT), ";" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "println", "(", EXPRESSION, ")" ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;




## Para utilizar a calculadora bastar rodar:

```
$ python3 main.py test1.c 
```
Sendo 'test1.c', um arquivo .c que contém a expressão que deseja calcular.

###### Ex 1:
```
$ python3 main.py test1.c
```

###### Ex arquivo test1.c:
```
x=5;
y=10;   
z=x+y;
println(z);
```






