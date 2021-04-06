import sys 
import string
import ast
from abc import ABC, abstractmethod

class Node(ABC):
    def __init___(self, value):
        super().init(value) 
    
    @abstractmethod
    def Evaluate(self):  
        pass

# Binary Operation
class BinOp(Node):
    
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self):
        # retorna a operação dos seus dois filhos:
        left = self.children[0].Evaluate()
        right = self.children[1].Evaluate()
        
        if self.value == "PLUS":
            return left + right
        elif self.value == "MINUS":
            return left - right
        elif self.value == "TIMES":
            return left * right
        elif self.value == "DIVIDE":
            return int(left / right)   
    
# Unary Operation
class UnOp(Node):
    def __init__(self, value):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self):
        # retorna o sinal do numero
        left = self.children[0].Evaluate()
        if self.value == "PLUS":
            return left
        if self.value == "MINUS":
            return -left
        

# Integer value 
class IntVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self):
        # retorna o próprio valor inteiro
        return self.value
        
# No Operation (Dummy)
class NoOp(Node):
    def Evaluate(self):
        pass

class Token:
    def __init__(self, tipo: str, value: int): 
        self.tipo = tipo
        self.value = value

class Tokenizer:
    def __init__(self, origin: str): # , position: int, actual : Token
        self.origin = origin     #codigo fonte que sera tokenizado
        self.position = 0       #posicao atual que o Tokenizador esta separando
        self.actual = Token(tipo = "", value=None)   #None  #ultimo token separado
        self.qtd = 0
         
    def selectNext(self):
        isNum = False
        isSpace = False
        number = ""

        if self.position == (len(self.origin)):
                token = Token("EOF", "")
                self.actual = token
                if (self.qtd != 0):
                    raise KeyError
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
        elif atual == "/":
            token = Token("DIVIDE", atual)
            self.actual = token
            self.position += 1
        elif atual == "*":
            token = Token("TIMES", atual)
            self.actual = token
            self.position += 1
        elif atual == "(":
            token = Token("ABRE", atual)
            self.actual = token
            self.position += 1
            self.qtd +=1
        elif atual == ")":
            token = Token("FECHA", atual)
            self.actual = token
            self.position += 1
            self.qtd -=1
            if self.position == (len(self.origin)):
                if (self.qtd != 0):
                    raise KeyError
                
        elif atual == " ":
            self.position += 1
            self.selectNext()
        else: 
            raise KeyError
        return    

class PrePro():
    
    def __init__(self, originPP: str): 
        self.originPP = originPP                     #codigo fonte que sera tokenizado
        self.positionPP = 0                          #posicao atual que o Tokenizador esta separando
        self.actual = Token(tipo = "", value=None)   #None  #ultimo token separado

    def filter(self):        
        atual = self.originPP[self.positionPP]
        tamanho = self.originPP 
        filtered = "" #nova string filtrada

        #Ideia de como remover comentarios em um unico loop retirada do GeeksforGeeks
        #https://www.geeksforgeeks.org/remove-comments-given-cc-program/
        isComment = False
        isClosed = False

        while self.positionPP < (len(self.originPP)):    

            #se estiver em comenentario, checar o fim dele
            if (isComment and self.originPP[self.positionPP] == '*' and self.originPP[self.positionPP +1] == '/'):
                isComment = False
                isClosed = True
                self.positionPP +=1
            
            #checar o inicio de comentario
            elif (self.originPP[self.positionPP] == '/' and self.originPP[self.positionPP +1] == '*'):
                isComment = True

                self.positionPP +=1
            elif (not isComment):
                filtered += self.originPP[self.positionPP]

            self.positionPP +=1

        #Caso tenha aberto um comentario mas nao fechado
        if (isComment and not isClosed):
            raise KeyError
        return filtered
       

class Parser():

    def __init__(self):
        pass

    def factor(self):
              
        # print("TIPO_f: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
        if (self.tokens.actual.tipo == "INT" ):
            arvore = IntVal(self.tokens.actual.value)
            self.tokens.selectNext()
        elif (self.tokens.actual.tipo == "PLUS" ): 
            arvore = UnOp(value="PLUS")
            self.tokens.selectNext()
            arvore.children[0] = self.factor()

        elif (self.tokens.actual.tipo == "MINUS" ):
            arvore = UnOp(value="MINUS")
            self.tokens.selectNext()
            arvore.children[0] = self.factor()
            
        elif (self.tokens.actual.tipo == "ABRE" ):          
            self.tokens.selectNext()
            arvore = self.parseExpression()
            if (self.tokens.actual.tipo != "FECHA" ):
                raise KeyError
            else:
                self.tokens.selectNext()
        else:
            raise KeyError
 
        return arvore
        

    def term(self):
        arvore = self.factor()          
    
        #int com int da erro
        if (self.tokens.actual.tipo == "INT"):
            raise KeyError

        while(self.tokens.actual.tipo == "TIMES" or self.tokens.actual.tipo == "DIVIDE"):
            tipo = self.tokens.actual.tipo
            if tipo == "TIMES":
                self.tokens.selectNext()
                arvore_copy = BinOp("TIMES")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.factor()
                arvore = arvore_copy

            elif tipo == "DIVIDE":
                self.tokens.selectNext()
                arvore_copy = BinOp("DIVIDE")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.factor()
                arvore = arvore_copy
            else:
                raise KeyError
        return arvore
    
    def parseExpression(self):

        arvore = self.term()
        tipo = ""
        while(self.tokens.actual.tipo == "PLUS" or self.tokens.actual.tipo == "MINUS"  ):
            tipo = self.tokens.actual.tipo
            if tipo == "PLUS":
                self.tokens.selectNext()               
                arvore_copy = BinOp("PLUS")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.term()
                arvore = arvore_copy

            elif tipo == "MINUS":
                self.tokens.selectNext()
                arvore_copy = BinOp("MINUS")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.term()
                arvore = arvore_copy
            else:
                raise KeyError
        return arvore

    def run(self, code: str):
        preProce = PrePro(code)
        code = preProce.filter()
        self.tokens = Tokenizer(code)
        self.tokens.selectNext()
        resultado = ((self.parseExpression()))
        print(resultado.Evaluate())

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    expression = f.readline()
    compilador = Parser()

    # compilador.run(sys.argv[1]) 
    compilador.run(expression)






