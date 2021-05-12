#### Diagrama Sintático

[![Diagrama](https://i.imgur.com/jzcI291.png)]()  
[![Diagrama](https://i.imgur.com/jYCr270.png)]()


#### EBNF


BLOCK = "{", COMMAND, "}" ;   
COMMAND = ( λ | ASSIGNMENT | PRINT | BLOCK | WHILE | IF ), ";" ;  
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;                                            
PRINT = "println", "(", (EXPRESSION | NUMERO ), ")" ;                                
WHILE = "while", "(", EXPRESSION, ")", COMMAND, BLOCK ;  
IF = "if", "(", EXPRESSION, ")", (COMMAND | COMMAND, "else", COMMAND) ;  
OREXPR = ANDEXPR, { "||" } ;  
ANDEXPR = EQEXPR, { "&&" } ;  
EQEXPR = RELEXPR, { "==" } ;  
RELEXPR = EXPRESSION, { (">" | "<"), EXPRESSION } ;  
EXPRESSION = TERM, { ("+" | "-"), TERM } ;  
TERM = FACTOR, { ("*" | "/"), FACTOR } ;  
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMERO | IDENTIFIER | "(", EXPRESSION, ")" | "readln",  "(", ")" ;  
READLN = "readln", "(", ")" ;  
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;  
NUMERO = DIGIT, { DIGIT } ;  
LETTER = ( a | ... | z | A | ... | Z ) ;  
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;  




## Para utilizar a calculadora bastar rodar:

```
$ python3 main.py test1.c 
```
<<<<<<< HEAD
Sendo 'test1.c', um arquivo .c que contém a expressão que deseja calcular.
=======


###### Ex:
```
$ python3 main.py test1.c
```

<<<<<<< HEAD
###### Ex arquivo test1.c:
```
{
    i = 1;
    n = 4;
    while(i<n)
    {
        i = i + 1;
    }
    println(i);   
}
```

=======



>>>>>>> 5028d64c6a996d60433399a298e4872eddc91fde





