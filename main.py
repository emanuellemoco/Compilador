import sys 
import string
import time

class Token:
    def __init__(self, tipo: str, value: int): 
        self.tipo = tipo
        self.value = value

class Tokenizer:
    def __init__(self, origin: str): # , position: int, actual : Token
        self.origin = origin     #codigo fonte que sera tokenizado
        self.position = 0       #posicao atual que o Tokenizador esta separando
        self.actual = Token(tipo = "", value=None)   #None  #ultimo token separado
         
    def selectNext(self):
        isNum = False
        isSpace = False
        number = ""

        if self.position == (len(self.origin)):
                token = Token("EOF", "")
                self.actual = token
                return
        atual = self.origin[self.position]

        if atual.isnumeric():
            while self.position < (len(self.origin)) and (self.origin[self.position]).isnumeric():
                number += self.origin[self.position]
                self.position +=1
            token = Token("INT", int(number))
            self.actual = token
            
        elif atual == "+":
            token = Token("PLUS", atual)
            self.actual = token
            self.position += 1
        elif atual == "-":
            token = Token("MINUS", atual)
            self.actual = token
            self.position += 1
        elif atual == " ":
            self.position += 1
            self.selectNext()
        else: 
            token = Token("invalido", atual)
            self.actual = token
            self.position += 1
            raise KeyError
               
        # print("tipo: {}, valor: {}".format(self.actual.tipo, self.actual.value))
        return    
        

class Parser():
    
    def __init__(self):
        pass

    def parseExpression(self):
        resultado = 0
        while (self.tokens.actual.tipo != "EOF"):
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "INT":
                resultado = self.tokens.actual.value 
                self.tokens.selectNext()
                if self.tokens.actual.tipo == "INT":
                    raise KeyError
                while(self.tokens.actual.tipo == "PLUS" or self.tokens.actual.tipo == "MINUS" or self.tokens.actual.tipo == "INT" ):
                    if self.tokens.actual.tipo == "INT":
                        raise KeyError
                    if self.tokens.actual.tipo == "PLUS":
                        self.tokens.selectNext()
                        if self.tokens.actual.tipo == "INT":
                            resultado += self.tokens.actual.value
                        else:
                            raise KeyError
                    if self.tokens.actual.tipo == "MINUS":
                        self.tokens.selectNext()
                        if self.tokens.actual.tipo == "INT":
                            resultado -= self.tokens.actual.value
                        else:
                            raise KeyError
                    self.tokens.selectNext()
                print(resultado)
                return resultado
            else:
                raise KeyError
  
    def run(self, code: str):
        self.tokens = Tokenizer(code)
        self.parseExpression()

if __name__ == '__main__':
    compilador = Parser()
    compilador.run(sys.argv[1])

