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
    def __init__(self, value):
        self.value = value

    def Evaluate(self):
        return st.getter(self.value)
# ----------------------------------------------------------------
# Le somente inteiros
class Println(Node):
    def __init__(self):
        self.children = [None] * 2

    def Evaluate(self):
        print("TA ENTRANDO NO EVALUATE DO PRINT")
        left = self.children[0].Evaluate()
        print(left)
# ----------------------------------------------------------------
class Readln(Node):
    def __init__(self):
        self.children = [None] * 2

# eval chama o input convertendo para inteiro
    def Evaluate(self):
        print("ENTROU AQUI")
        value = input()
        if value.isnumeric():
            return int(value)
        else:
            raise KeyError 

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
            return (int(left / right))   

        #Operadores relacionais 
        if self.value == "GREATER":
            return (int(left > right))
        elif self.value == "LESS":
            return (int(left < right))
        elif self.value == "RELATIVE":
            return (int(left == right))

        #Operadores booleanos 
        if self.value == "AND":
            return (left and right)
        elif self.value == "OR":
            return (left or right)


        #Atribuicao
        elif self.value == "ASSIGMENT":
            print("--------> ASSIGMENT")
            print("entrou aqui, left: {} right: {} ".format(left,right))
            st.setter(left, right)
            return



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
        if self.value == "NEG": 
            return (not left)

# ----------------------------------------------------------------    
class WhileOp(Node):
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 2

    def Evaluate(self):
        left = self.children[0].Evaluate()      #Condicao
        right = self.children[1].Evaluate()

        while (left):
            # chama command
            right = self.children[1].Evaluate() 

#consulta o no a esquerda, que é o no de condicao
#retorna 0 ou 1
#se 0, termina
#se 1, chama o command (da eval no command que retorna que terminou) 
#e roda o comando do while

# ----------------------------------------------------------------    
class IfOp(Node):
    def __init__(self, value=None):            
        self.value = value
        self.children = [None] * 3

    def Evaluate(self):
        print("0 =>", self.children[0])

        left = self.children[0].Evaluate()      # Condition
        # middle = self.children[1].Evaluate()    # Command
        # right = self.children[2].Evaluate()     #else - pode nao existir

        #consulta 0, se for verdade da eval no filho 1
        if (left):
            middle = self.children[1].Evaluate() #?????
            return 
        elif (self.children[2] != None) :
            right = self.children[2].Evaluate()  
            return
            #checar se o filho [2] existe, se exitir chama o seu eval 


#consulta o no a esquerda, que é o no de condicao
# recebe uma resposta, se for verdade
# da eval no filho do meio [1]

# se o filho 2 existir, chama o seu eval, 
# caso nao, retorna.



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
        self.qtdPar = 0            # quantidade de parenteses
        self.qtdCha = 0            # quantidade de chaves
         
    def selectNext(self):
        number = ""
        expression = ""
        if self.position == (len(self.origin)):
                token = Token("EOF", "")
                self.actual = token
                if (self.qtdPar != 0 or self.qtdCha != 0):
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

            elif expression == "readln":
                token = Token("READ", expression)
                self.actual = token
            elif expression == "while":
                token = Token("WHILE", expression)
                self.actual = token
            elif expression == "if":
                token = Token("IF", expression)
                self.actual = token
            elif expression == "else":
                token = Token("ELSE", expression)
                self.actual = token

            else:
                token = Token("IDENTIFIER", expression)
                self.actual = token
        
        
        elif atual == "=":
            self.position +=1
            if self.origin[self.position] == "=":
                token = Token("RELATIVE", atual) # ==
                self.actual = token
                self.position += 1
            else:
                token = Token("EQUAL", atual)
                self.actual = token
                # self.position += 1
        
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

        elif atual == ">":
            token = Token("GREATER", atual)
            self.actual = token
            self.position += 1
        elif atual == "<":
            token = Token("LESS", atual)
            self.actual = token
            self.position += 1
        elif atual == "&":
            self.position +=1
            if self.origin[self.position] == "&":
                token = Token("AND", atual)
                self.actual = token
                self.position += 1
            else:
                raise KeyError
        elif atual == "|":
            self.position +=1
            if self.origin[self.position] == "|":
                token = Token("OR", atual)
                self.actual = token
                self.position += 1
            else:
                raise KeyError
        elif atual == "!":
            token = Token("NEG", atual)
            self.actual = token
            self.position += 1




        elif atual == "(":
            token = Token("ABRE_PAR", atual)
            self.actual = token
            self.position += 1
            self.qtdPar +=1
        elif atual == ")":
            token = Token("FECHA_PAR", atual)
            self.actual = token
            self.position += 1
            self.qtdPar -=1
            if self.position == (len(self.origin)):
                if (self.qtdPar != 0):
                    raise KeyError                
        elif atual == " ":
            self.position += 1
            self.selectNext()
    
        elif atual == "\n":
            self.position += 1
            self.selectNext()

    #TALVEZ TER QUE CHECAR QUANTIDADE DE CHAVES
        elif atual == "{":
            token = Token("ABRE_CHA", atual)
            self.actual = token
            self.position += 1
            self.qtdCha +=1
        elif atual == "}":
            token = Token("FECHA_CHA", atual)
            self.actual = token
            self.position += 1
            self.qtdCha -=1
            if self.position == (len(self.origin)):
                if (self.qtdCha != 0):
                    raise KeyError     
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
        
        # print("TIPO_b: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

        if (self.tokens.actual.tipo == "ABRE_CHA"):
            
            while(self.tokens.actual.tipo != "FECHA_CHA"):
                self.tokens.selectNext()    
                # Se chegar um EOF e não tiver fechado a chave, da erro
                if (self.tokens.actual.tipo == "EOF"):
                    raise KeyError    
                
                arvore = self.Command()
                print("tree: ", arvore)
                return arvore
                
        print("ta retornando", arvore)
        return arvore

# ----------------------------------------------------------------
    def Command(self):
        variavel = ""
        print("TIPO_c: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))
        time.sleep(1)
    # 2 casos:
    # Se token for IDENT EQUAL EXP terminando em SEMICOLON
        if self.tokens.actual.tipo == "IDENTIFIER":
            print("command - é identifier")
            # variavel = self.tokens.actual.value
            variavel = IdentfOp(self.tokens.actual.value)
            
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "EQUAL":
                self.tokens.selectNext()
                arvore = self.orExpression()
                arvore_copy = BinOp("ASSIGMENT")
                print("chegou aqui")
                arvore_copy.children[0] = variavel
                arvore_copy.children[1] = arvore

                return arvore_copy
                if (self.tokens.actual.tipo == "SEMICOLON"):
                    print("AAAAAAAAAAA")
                    # return NoOp()
                    NoOp()
                    self.tokens.selectNext()
                    
            if self.tokens.actual.tipo == "ABRE_PAR":
                raise KeyError;
                      

        # Se token for PRINT EQUAL ABRE EXP FECHA terminando em SEMICOLON   
        elif self.tokens.actual.tipo == "PRINT":
            # print("é print")
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                print("ABRIU")
                self.tokens.selectNext()
                arvore = (self.orExpression())
                test = Println()
                test.children[0] = arvore
                # test.Evaluate()
                if (self.tokens.actual.tipo == "FECHA_PAR"):
                    print("FECHOU")
                    self.tokens.selectNext()
                    if (self.tokens.actual.tipo == "SEMICOLON"):
                        return arvore
                    else:
                        raise KeyError
                
        



        elif self.tokens.actual.tipo == "WHILE":
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                arvore = (self.orExpression()) #??????????
                self.tokens.selectNext()

                if (self.tokens.actual.tipo == "FECHA_PAR"):
                    self.tokens.selectNext()
                    arvore = self.WhileOp()
                    self.tokens.selectNext()

                    arvore_copy.children[0] = arvore
                    arvore_copy.children[1] = self.WhileOp()
                    arvore = arvore_copy

                    return arvore


        elif self.tokens.actual.tipo == "IF":
            print("é if")
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                self.tokens.selectNext()
                print("-> 1")
                arvore = (self.orExpression())
                print("-> 2")
                test = IfOp()
                test.children[0] = arvore
                test.children[1] = self.Command()
                self.tokens.selectNext()
                if (self.tokens.actual.tipo == "ELSE"):
                    test.children[2] = self.Command()

                test.Evaluate()
                if (self.tokens.actual.tipo == "FECHA_PAR"):
                    self.tokens.selectNext()
                    if (self.tokens.actual.tipo == "SEMICOLON"):
                        return arvore
                    else:
                        raise KeyError
               
        elif (self.tokens.actual.tipo == "ABRE_CHA" or self.tokens.actual.tipo == "FECHA_CHA" ):
            return


        else:
            #BLOCK
            arvore = (self.Command())
            print("---------------")
        
                

#______________________________________________________________    
    def orExpression(self):
        arvore = self.andExpression()
        while(self.tokens.actual.tipo == "OR"):
            self.tokens.selectNext()               
            arvore_copy = BinOp("OR")
            arvore_copy.children[0] = arvore
            arvore_copy.children[1] = self.andExpression()
            arvore = arvore_copy
        return arvore

#______________________________________________________________ 
    def andExpression(self):
        arvore = self.eqExpression()
        while(self.tokens.actual.tipo == "AND"):
            self.tokens.selectNext()               
            arvore_copy = BinOp("AND")
            arvore_copy.children[0] = arvore
            arvore_copy.children[1] = self.eqExpression()
            arvore = arvore_copy
        return arvore


#______________________________________________________________ 
    def eqExpression(self):
        arvore = self.relExpression()
        while(self.tokens.actual.tipo == "RELATIVE"):
            self.tokens.selectNext()               
            arvore_copy = BinOp("RELATIVE")
            arvore_copy.children[0] = arvore
            arvore_copy.children[1] = self.relExpression()
            arvore = arvore_copy
        return arvore


#______________________________________________________________   
    def relExpression(self):
        arvore = self.parseExpression()
        tipo = "" 
        while(self.tokens.actual.tipo == "GREATER" or self.tokens.actual.tipo == "LESS"  ):
            tipo = self.tokens.actual.tipo
            if tipo == "GREATER":
                self.tokens.selectNext()               
                arvore_copy = BinOp("GREATER")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.parseExpression()
                arvore = arvore_copy

            elif tipo == "LESS":
                self.tokens.selectNext()
                arvore_copy = BinOp("LESS")
                arvore_copy.children[0] = arvore
                arvore_copy.children[1] = self.parseExpression()
                arvore = arvore_copy
            else:
                raise KeyError
        return arvore
    

#______________________________________________________________    
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
#______________________________________________________________

    def term(self):
        arvore = self.factor()          

    
        #int com int da erro
        if (self.tokens.actual.tipo == "INT"):
            raise KeyError
        if (self.tokens.actual.tipo == "IDENTIFIER"):
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

#______________________________________________________________
    def factor(self):
        print("TIPO_f: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

        #number:
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

        elif (self.tokens.actual.tipo == "NEG" ):
            arvore = UnOp(value="NEG")   ##implementar essa parte
            self.tokens.selectNext()
            arvore.children[0] = self.factor() 
            
        elif (self.tokens.actual.tipo == "ABRE_PAR" ):          
            self.tokens.selectNext()
            arvore = self.orExpression()  ########antes chamava a parseExpression
            if (self.tokens.actual.tipo != "FECHA_PAR" ):
                raise KeyError
            else:
                self.tokens.selectNext()

        elif (self.tokens.actual.tipo == "IDENTIFIER" ):
            arvore = IdentfOp(self.tokens.actual.value)
            # valor = arvore.Evaluate()        #acho que nao faz isso
            self.tokens.selectNext()
  
        elif self.tokens.actual.tipo == "READ":
            print(" f ---> read")
            self.tokens.selectNext()
            if self.tokens.actual.tipo == "ABRE_PAR":
                print(" f ---> abre par")
                self.tokens.selectNext()
                if self.tokens.actual.tipo == "FECHA_PAR":
                    print(" f ---> fecha par")
                    arvore = Readln()
                    self.tokens.selectNext()
        

        else:
            print("TIPO_else: {}, VALOR: {}".format(self.tokens.actual.tipo, self.tokens.actual.value))

            raise KeyError
 
        return arvore
#______________________________________________________________


    def run(self, code: str):
        preProce = PrePro(code)
        code = preProce.filter()
        self.tokens = Tokenizer(code)
        self.tokens.selectNext()
        resultado = self.Block()
        # print(resultado)
        print("odios")
        print(resultado.Evaluate()) ## nao deveria fazer evaluate aqui??


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
