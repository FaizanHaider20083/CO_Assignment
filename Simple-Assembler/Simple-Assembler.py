import sys
code = []

def convert_to_binary(a):
    stri = ""
    while(a>0):
        stri += str(a%2)
        a = a//2
    return stri[::-1]

def convert_to_decimal(a):
    num  = 0
    i =0
    for char in a[::-1]:
        

        num += (2**i)*int(char)
        
        i += 1
    return num


print(convert_to_decimal(convert_to_binary(32)))

def andfunc(a,b):
    return a and b

def mul(a,b):
    return a*b

def divide(a,b):
    return a/b
def orfunc(a,b):
    return a or b

def left_shift(a,b):
    b = convert_to_binary(b)
    string  = a[len(b)::]
    string += str(a)
    return a

def right_shift(a,b):
    string = convert_to_binary(b)
    for i in a[:len(a) - len(b):]:
        string += str(i)
    return string 

def invert(a):
    string = ""
    for i in convert_to_binary(a):
        if i == '1':
            string += "0"
        else :
            string += "1"
    return string

if __name__ == "__main__":
    print("Hello Assembler")
    i = 0
    for line in sys.stdin:
    
        code.append(line.strip())
        if line.strip() == 'hlt':
            for coding in code:
                print(coding)

            break

