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
            # token = Token("invalido", atual)
            # self.actual = token
            # self.position += 1
            raise KeyError
        return    

class PrePro():
    
    def __init__(self, originPP: str): # , position: int, actual : Token
        self.originPP = originPP     #codigo fonte que sera tokenizado
        self.positionPP = 0       #posicao atual que o Tokenizador esta separando
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

        expressao = 0
        
        # print("TIPO_f: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
        if (self.tokens.actual.tipo == "INT" ):
            expressao = self.tokens.actual.value
            self.tokens.selectNext()
        elif (self.tokens.actual.tipo == "PLUS" ):
           self.tokens.selectNext()
           expressao += self.factor()
        elif (self.tokens.actual.tipo == "MINUS" ):
           self.tokens.selectNext()
           expressao -= self.factor()

        elif (self.tokens.actual.tipo == "ABRE" ):
            # self.qtd +=1
            # print("qtd_a: ", self.qtd)
            
            self.tokens.selectNext()
            expressao += self.parseExpression()
            if (self.tokens.actual.tipo != "FECHA" ):
                raise KeyError
            else:
                self.tokens.selectNext()
        else:
            raise KeyError
 

        return expressao
        

    def term(self):
        resultado = self.factor()

        # print("TIPO_t: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))


        # if (self.tokens.actual.tipo == "FECHA"):
        #     self.qtd -=1
        #     print("qtd_f_t: ", self.qtd)
            


        #int com int da erro
        if (self.tokens.actual.tipo == "INT"):
            raise KeyError

        while(self.tokens.actual.tipo == "TIMES" or self.tokens.actual.tipo == "DIVIDE"  ):
            
            tipo = self.tokens.actual.tipo
            if tipo == "TIMES":
                self.tokens.selectNext()
                resultado *= self.factor()
            elif tipo == "DIVIDE":
                self.tokens.selectNext()
                resultado /= self.factor()
            else:
                raise KeyError
        return resultado
    
    def parseExpression(self):
        resultado = self.term()
        tipo = ""
        
        # print("TIPO_e: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

        # if (self.tokens.actual.tipo == "FECHA"):
        #     self.qtd -=1
        #     print("qtd_f_e: ", self.qtd)


        while(self.tokens.actual.tipo == "PLUS" or self.tokens.actual.tipo == "MINUS"  ):
            tipo = self.tokens.actual.tipo
            if tipo == "PLUS":
                self.tokens.selectNext()
                resultado += self.term()
            elif tipo == "MINUS":
                self.tokens.selectNext()
                resultado -= self.term()
            else:
                raise KeyError
        return resultado

    def run(self, code: str):
        preProce = PrePro(code)
        code = preProce.filter()

        self.tokens = Tokenizer(code)
        self.tokens.selectNext()
        resultado = (int(self.parseExpression()))
        # if (self.qtd != 0):
        #     raise KeyError
        print(resultado)

if __name__ == '__main__':
    compilador = Parser()
    compilador.run(sys.argv[1])



