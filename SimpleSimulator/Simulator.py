from sys import stdin

instructions = {"00010":'B',"10011":'F'}
registers = {"000":"0"*16,"001":"0"*16,"010":"0"*16,"011":"0"*16,"100":"0"*16,"101":"0"*16,"110":"0"*16,"111":"0"*16}
program_counter = 0

def convert_to_binary(a):
    stri = ""
    while(a>0):
        stri += str(a%2)
        a = a//2
    return stri[::-1]


def input():
    binary = open("binary.txt",'w')
    try:
        for line in stdin:
            binary.write(line )
            if ("1001100000000000" in line):
                return
    except EOFError:
        binary.close()

def memory_dump():
    line_number = 0
    binary = open("binary.txt",'r')
    for line in binary.readlines():
        print(line,end="")
        line_number += 1
    for i in range(line_number,257):
        print("0"*16)
    binary.close()



def process():
    global instructions
    global program_counter
    binary = open("binary.txt",'r')
    for line in binary.readlines():
        command = line[0:5]
        category = instructions[command]
        output(category,line)
        program_counter += 1
    binary.close()


def output(category,line):
    if (category == 'F'):
        printregisters()
        return
    elif (category == 'B'):
        if (line[0:5] == "00010"):
            mov_register_imm(line)
            printregisters()
            

def mov_register_imm(line):
    global registers
    reg = line[5:8]
    registers[reg] = line[8:]


def printregisters():

    print_programcounter()
    for register in registers:
        print(registers[register],end =" ")
   
def print_programcounter():
    global program_counter
    print(convert_to_binary(program_counter),end =" ")

if (__name__ == '__main__'):
    input()
    process()
    memory_dump()
        