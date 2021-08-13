import sys

# for line in sys.stdin:
#     if not line.strip():
#         print("yeah")

insOpcodes= {"add": "00000", "sub": "00001", "mov":"00010", "mov_r":"00011", "ld": "00100", "st": "00101" }
registerAddress= {"R0":"000", "R1": "001", "R2": "010", "R3": "011", "R4":"100", "R5":"101", "R6":"110"}

insElements  ={"add": 4, "sub": 4, "mov": 3, "mov_r": 3, "ld": 3, "st": 3 }


def typeA (line):
    list= line.split()
    str= ""
    c=0

    for i in list[1:]:
        if i in registerAddress:
            str+= registerAddress[i]
            c+=1
        
    if c!=3:
        str= "Typos in register name."
        return
    print (str)
    return

# def Subtraction (line):
#     list= line.split()
#     str= ""
    
#     for i in list[1:]:
#         if i in registerAddress:
#             str+= registerAddress[i]
#         else:
#             str= "Typos in register name."
    
#     print (str)
#     return


line= "sub R1 r3 R0  df"
list= line.split()
Subtraction(line)
str= ""

print(list[1:])


def checkSyntax(line):
    list= line.split()
    str= ""
    if( list.length  != insElements[list[0]]):
        
        str= "Wrong syntax used for instructions."
        return str

def checkTypos(line):
    list= line.split()
    str= ""

    if list[0] not in insOpcodes:
        str= "Typos in instruction name."
    return str

def opcodes(line):
    str=""
    list= line.split()
    if list[0] in insOpcodes:
            str+= insOpcodes[list[0]]

    return str

