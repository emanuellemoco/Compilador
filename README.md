# Status dos testes
![git status](http://3.129.230.99/svg/emanuellemoco/Compilador/)



#### Diagrama Sintático

[![Diagrama](https://i.imgur.com/iG9kJrb.jpeg)]()  



#### EBNF


BLOCK = "{", COMMAND, "}" ;   
COMMAND = ( (ASSIGNMENT | PRINT | DECLARATION ), ";" )  | ( λ | BLOCK | WHILE | IF ) ;  
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;   
DECLARATION = ( "int" |  "bool" | "string" ),  IDENTIFIER ";" ;                                       
PRINT = "println", "(", (EXPRESSION | NUMBER ), ")" ;                                
WHILE = "while", "(", EXPRESSION, ")", COMMAND, BLOCK ;  
IF = "if", "(", EXPRESSION, ")", (COMMAND | COMMAND, "else", COMMAND) ;  
OREXPR = ANDEXPR, { "||" } ;  
ANDEXPR = EQEXPR, { "&&" } ;  
EQEXPR = RELEXPR, { "==" } ;  
RELEXPR = EXPRESSION, { (">" | "<"), EXPRESSION } ;  
EXPRESSION = TERM, { ("+" | "-"), TERM } ;  
TERM = FACTOR, { ("*" | "/"), FACTOR } ;  
FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | IDENTIFIER | "(", EXPRESSION, ")" | "readln",  "(", ")" | STRING | BOOL ;  
READLN = "readln", "(", ")" ;  
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;    
NUMBER = DIGIT, { DIGIT } ;  
STRING = """, "LETTER", { LETTER | DIGIT | "_" }, """;   
BOOL = "true" | "false" ;   
LETTER = ( a | ... | z | A | ... | Z ) ;    
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;    




## Para utilizar a calculadora bastar rodar:

```
$ python3 main.py test1.c 
```


Sendo 'test1.c', um arquivo .c que contém a expressão que deseja calcular.


###### Ex:
```
$ python3 main.py test1.c
```

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





