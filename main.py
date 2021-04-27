import sys 
import string
import ast
from abc import ABC, abstractmethod
import time
import os

symbol_table_dict = {}
class SymbolTable():
    #cria um dicionario
    def __init__(self): 
        pass

    def getter(self, variable):        
        # vai dar problema se tentar buscar uma variavel que nao existe
        if variable in symbol_table_dict:
            #retornar o valor
            return symbol_table_dict[variable]
        else:
            raise KeyError

    #por enquanto as variaveis sao unicas, nao havera problema de sobrescrita
    def setter(self, variable, value):
        # if symbol not in symbol_table_dict:           #NAO SEI SE VAI PRECISAR
        symbol_table_dict[variable] = value;

st = SymbolTable()
# ----------------------------------------------------------------
class Node(ABC):
    def __init___(self, value):
        super().init(value) 
    
    @abstractmethod
    def Evaluate(self):  
        pass
# ----------------------------------------------------------------
#faz o getter na symbol table 
class IdentfOp(Node):
    def __init__(self, values):
        self.value = values

    def Evaluate(self):
        return st.getter(self.value)
# ----------------------------------------------------------------
class Println(Node):
    def __init__(self):
        self.children = [None] * 2

    def Evaluate(self):
        left = self.children[0].Evaluate()
        print(left)

# ----------------------------------------------------------------
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

# ----------------------------------------------------------------    
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
        
# ----------------------------------------------------------------
# Integer value 
class IntVal(Node):
    def __init__(self, value=None):        
        self.value = value

    def Evaluate(self):
        # retorna o próprio valor inteiro
        return self.value
# ----------------------------------------------------------------       
# No Operation (Dummy)
class NoOp(Node):
    def Evaluate(self):
        pass
# ----------------------------------------------------------------
class Token:
    def __init__(self, tipo: str, value: int): 
        self.tipo = tipo
        self.value = value
# ----------------------------------------------------------------
class Tokenizer:

    def __init__(self, origin: str): # , position: int, actual : Token
        self.origin = origin     #codigo fonte que sera tokenizado
        self.position = 0       #posicao atual que o Tokenizador esta separando
        self.actual = Token(tipo = "", value=None)   #None  #ultimo token separado
        self.qtd = 0
         
    def selectNext(self):
        number = ""
        expression = ""
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


        elif atual.isalpha():
            while self.position < (len(self.origin)) and  ( self.origin[self.position].isalpha() or self.origin[self.position].isnumeric() or self.origin[self.position]=="_" ):
                expression += self.origin[self.position]
                self.position +=1
            if expression == "println":
                token = Token("PRINT", expression)
                self.actual = token
            else:
                token = Token("IDENTIFIER", expression)
                self.actual = token
        
        
        elif atual == "=":
            token = Token("EQUAL", atual)
            self.actual = token
            self.position += 1
        
        elif atual == ";":
            token = Token("SEMICOLON", atual) 
            self.actual = token
            self.position += 1

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
    
        elif atual == "\n":
            self.position += 1
            self.selectNext()
        else: 
            raise KeyError
        return    

# ----------------------------------------------------------------
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
       

# ----------------------------------------------------------------
class Parser():

    def __init__(self):
        pass

# ----------------------------------------------------------------
    # chama command 
    def Block(self):
        while(self.tokens.actual.tipo != "EOF"):           
            self.Command()
            self.tokens.selectNext()

# ----------------------------------------------------------------
    def Command(self):
        variavel = ""

    # 2 casos:
    # Se token for IDENT EQUAL EXP terminando em SEMICOLON
        if self.tokens.actual.tipo == "IDENTIFIER":
            variavel = self.tokens.actual.value
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "EQUAL":
                self.tokens.selectNext()
                
                arvore = (self.parseExpression())
                nos = (arvore.Evaluate())
                st.setter(variavel, nos)
                return arvore
                if (self.tokens.actual.tipo == "SEMICOLON"):
                    return NoOp()
                    

        # Se token for PRINT EQUAL ABRE EXP FECHA terminando em SEMICOLON   
        elif self.tokens.actual.tipo == "PRINT":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE":
                self.tokens.selectNext()

                arvore = (self.parseExpression())
                nos = (arvore.Evaluate())

                test = Println()
                test.children[0] = arvore
                test.Evaluate()
                
                if (self.tokens.actual.tipo == "FECHA"):
                    self.tokens.selectNext()
                    if (self.tokens.actual.tipo == "SEMICOLON"):
                        return
                
#______________________________________________________________
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

        elif (self.tokens.actual.tipo == "IDENTIFIER" ):
            arvore = IdentfOp(self.tokens.actual.value)
            valor = arvore.Evaluate()        
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
        resultado = self.Block()


if __name__ == '__main__':
    f = open(sys.argv[1], "r")

    #caso o arquivo esteja vazio nao faz nada:
    if (os.stat(sys.argv[1]).st_size == 0):
        pass
    else: 
        expression = []
        expression.append(f.read())
        compilador = Parser()
        compilador.run(expression[0])
