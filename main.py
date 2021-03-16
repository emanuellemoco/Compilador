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
        elif atual == "/":
            token = Token("DIVIDE", atual)
            self.actual = token
            self.position += 1
        elif atual == "*":
            token = Token("TIMES", atual)
            self.actual = token
            self.position += 1
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
        proximoF = self.originPP[self.positionPP +1]
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

    def term(self):
        ###checar se o proximo token é DIVIDE ou TIMES
       
       
        #pegar o numero
        self.tokens.selectNext()
        # print("TIPO_A: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
        numero = self.tokens.actual.value  #4
        self.tokens.selectNext()
        
        
        

        #verifica se é DIVIDE ou TIMES, se nao for, volta 
        while (self.tokens.actual.tipo == "DIVIDE" or self.tokens.actual.tipo == "TIMES"):
            tipo = self.tokens.actual.tipo 
            self.tokens.selectNext()    
            atual = self.tokens.actual.value 


            #aqui faz divisao e bota em resultado
            if (tipo == "DIVIDE"):
                return numero / atual 

            elif (tipo == "TIMES"):
                return numero * atual


        return numero
       
    
    def parseExpression(self):
        resultado = 0
        tipo = ""
        while (self.tokens.actual.tipo != "EOF"):
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "INT":
                resultado = self.tokens.actual.value
                self.tokens.selectNext()

                #se for int int -> erro
                if self.tokens.actual.tipo == "INT":
                    raise KeyError
                
                #para tratar quando o primeiro caso é divisao ou vezes
                if (self.tokens.actual.tipo == "TIMES" or self.tokens.actual.tipo == "DIVIDE" ):
                    tipo = self.tokens.actual.tipo
                    a = self.term()
                    if tipo== "TIMES":
                        resultado *= a

                    if tipo== "DIVIDE":
                        resultado -= a
                
                while(self.tokens.actual.tipo == "PLUS" or self.tokens.actual.tipo == "MINUS"  ):
                    tipo = self.tokens.actual.tipo
                    a = self.term()
      
                    try:
                        if tipo== "PLUS":
                            resultado += a
                        

                        if tipo== "MINUS":
                            resultado -= a
                    except:
                        raise KeyError
                                        
                print("FIM: ",resultado)
                return resultado
            else:
                raise KeyError
  
    def run(self, code: str):
        preProce = PrePro(code)
        code = preProce.filter()

        self.tokens = Tokenizer(code)
        self.parseExpression()

if __name__ == '__main__':
    compilador = Parser()
    compilador.run(sys.argv[1])



