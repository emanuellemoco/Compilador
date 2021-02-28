import sys 
import string

expression = " ".join(sys.argv[1:])
# print("Expression: {}".format(expression))

end = len(expression)
result = 0
number = 0
i=0

isNum = False
isSpace = False

for i in reversed(range(len(expression))):

    #Caso ocorra espaços entre números
    if isNum and isSpace:
        if expression[i].isnumeric():
            raise KeyError

    if not isNum:
        isNum = expression[i].isnumeric()

    if expression[i] == " " and isNum:
        isSpace = True
    
    if expression[i] == "+" or expression[i] == "-":
        if not isNum:
            raise KeyError
        isSpace = False
        isNum = False
        number = int((expression[i+1:end]))
        if expression[i] == "+":
            result += number
        if expression[i] == "-":
            result -= number
        end = i
    

#Para pegar o primeiro valor:
i=0
for i in range(len(expression)):
    # print (expression[i])
    if expression[0] == "+" or expression[0] == "-":
        raise KeyError

    if expression[0] != "+" and expression[0] != "-":
        if expression[i] == "+" or expression[i] == "-":
            result += int(expression[0:i])
            break

print("Result: {}".format(result))





