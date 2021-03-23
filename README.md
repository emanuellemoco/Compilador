#### Diagrama Sintático

[![Diagrama](https://i.imgur.com/B3uIJgp.png)]()


#### EBNF

EXPRESSION = NUMBER, {("+" | "-" | "*" | "/" | "(") | ")", NUMBER} ;

Sendo NUMBER qualquer número, ou seja:



## Para utilizar a calculadora bastar rodar:

```
$ python3 main.py 'expressão' 
```
Sendo 'expressão', a expressão que deseja calcular. 

###### Ex 1:
```
$ python3 main.py ' /* a */ 1 /* b */ '
```

######  Ex 2:
```
$ python3 main.py ' 3-2 '
```

######  Ex 3:
```
python3 main.py ' 11+22-33 /* a */ '
```

######  Ex 3:
```
python3 main.py ' 4/2+3 '
```







