from sys import stdin
import matplotlib.pyplot as plt

instructions = {"00000":'A',"00001":'A',"00010":'B',"00011":'C',"00100":'D',"00101":'D',"00110":'A',"00111":'C',"01000":'B',"01001":'B',"01010":'A',"01011":'A',"01100":'A',"01101":'C',"01110":'C',"01111":'E',"10000":'E',"10001":'E',"10010":'E',"10011":'F'}
registers = {"000":"0"*16,"001":"0"*16,"010":"0"*16,"011":"0"*16,"100":"0"*16,"101":"0"*16,"110":"0"*16,"111":"0"*16}
program_counter = 0
variables = {}
flag_reset = 0
flag_pass = 0
contd=0
memory_addresses=[]
def convert_to_decimal(a):   #to convert to decimal 
    num  = 0
    i =0
    for char in a[::-1]:
        

        num += (2**i)*int(char)
        
        i += 1
    return num

def convert_to_binary(a):   #to convert to binary
    stri = ""
    while(a>0):
        stri += str(a%2)
        a = a//2
    return stri[::-1]


def input():
    binary = open("binary.txt",'w')           #opens the binary file
    try:
        for line in stdin:
            binary.write(line )               #writes the binary instructions into the file
            if ("1001100000000000" in line):  #to return once the halt is reached
                return 
    except EOFError:

        binary.close()
        


def memory_dump():
    line_number = 0
    binary = open( "binary2.txt",'r')
    for line in binary.readlines():
        if ("1001100000000000" != line):
            print(line,end="")
            line_number += 1
        else:
            print("1001100000000000")
            line_number += 1

    for var in variables:
        print(variables[var])
        line_number += 1
    for i in range(line_number,256):
        print("0"*16)
    binary.close()



def process():
    global instructions
    global program_counter
    global memory_addresses
    binary = open("binary.txt",'r')
    binary2 = open("binary2.txt", 'w')
    for line in binary.readlines():
        command = line[0:5]
        category = instructions[command]
        #print("//////////////////",category,command,"//////////////////")
        output(category,line)
        binary2.write(line)
        #memory_addresses.append(convert_to_decimal(line[8:16]))
        memory_addresses.append(program_counter)
        program_counter += 1

    binary.close()
    binary2.close()


    
    
    
def output(category,line):
    global flag_reset
    global flag_pass
    global program_counter

    if (category == 'F'):
        printregisters()
        return
    elif (category == 'B'):
        if (line[0:5] == "00010"):
            mov_register_imm(line)
        elif (line[0:5] == "01000"):
            right_shift(line)
        
        elif(line[0:5] == "01001"):
            left_shift(line)
            

    elif (category == 'A'):
        if (line[0:5] == "00000"):
            add(line)
        elif (line[0:5] == "00001"):
            substract(line)

        elif(line[0:5] == "00110"):
            multiply(line)

        elif(line[0:5] == "01011"):
            Or(line)

        elif(line[0:5] == "01010"):
            xor(line)

        elif(line[0:5] == "01100"):
            And(line)
        
            

    elif (category == 'C'):
        if(line[0:5] == "00011"):
            mov_reg(line)

        elif(line[0:5] == "00111"):
            divide(line)

        elif (line[0:5] == "01101"):
            invert(line)

        elif (line[0:5] == "01110"):
            compare(line)

    elif(category == 'D'):
        if(line[0:5] == "00101"):
            store(line)

            
            
    elif (category == 'E'):
        global contd
        jmp=0
        flag= registers['111']
        if (line[0:5]== "10000"):   # inst : jump if less than
            if (flag[13]==1 ):      # if L=1, jump
                jmp= 1
        elif (line[0:5]== "10001"): # inst : jump if greater than
            if (flag[14]==1 ):      # if G=1, jump
                jmp= 1
        elif (line[0:5]== "10010"): # inst : jump if greater than
            if (flag[15]==1 ):      # if E=1, jump
                jmp= 1
        else: # that is, line[0:5]== "01111",  inst : jump
            jmp=1
        

        contd= program_counter  # PC value stored
        if jmp==1:
            jump(line)

        program_counter= contd  # PC value restored
            
            
            
            
    if(flag_reset == 1):
        if (flag_pass == 1):
            registers['111'] = '0'*16
            flag_reset = 0
            flag_pass  = 0
        else :
            flag_pass = 1

    printregisters()

    


def mov_reg(line):
    reg1 = line[10:13]
    reg2 = line[13:16]

    registers[reg1] = registers[reg2]
            

def mov_register_imm(line):
    global registers
    reg = line[5:8]

    imm = line[8:len(line)-1]
    imm = (16-len(imm))*'0' + imm
    registers[reg] = imm


def printregisters():

    print_programcounter()
    for register in registers:
        print(registers[register],end =" ")
    print("")
   
def print_programcounter():
    global program_counter
    bin = convert_to_binary(program_counter)
    bin = (8-len(bin))*'0' + bin
    print(bin,end =" ")

def add(line):
    global flag_pass
    reg2 = line[10:13]
    reg3 = line[13:16]
    total = convert_to_decimal(registers[reg2]) + convert_to_decimal(registers[reg3])
    reg1 = line[7:10]
    flag= registers['111']
    if(total<2^16-1):
        total = convert_to_binary(total)
        registers[reg1]  = ((16-len(total))*'0') + total 
    else:
        registers[reg1] = '0'*16
        flag= flag[0:11]+'1'+flag[13:]
        registers['111']=flag
        flag_pass=0
def substract(line):
    global flag_reset
    global flag_pass
    reg2 = line[10:13]
    reg3 = line[13:16]
    reg1 = line[7:10]
    total = convert_to_decimal(registers[reg2]) - convert_to_decimal(registers[reg3])
    flag= registers['111']
    if (total <0 ):
        registers[reg1] = '0'*16
        #print(flag[13:]+"      "+flag[12:])     
        flag= flag[0:11]+'1'+flag[13:]
        registers['111']=flag
        flag_pass=0
        return
        #setoverflow
    total = convert_to_binary(total)
    
    registers[reg1]  = ((16-len(total))*'0') + total 


def multiply(line):
    global flag_pass
    reg2 = line[10:13]
    reg3 = line[13:16]
    reg1 = line[7:10]
    total = convert_to_decimal(registers[reg2]) * convert_to_decimal(registers[reg3])
    flag= registers['111']
    if(total<2^16-1):
        total = convert_to_binary(total)
        registers[reg1]  = ((16-len(total))*'0') + total 
    else:
        registers[reg1] = '0'*16
        flag= flag[0:12]+'1'+flag[13:]
        registers['111']=flag
        flag_pass=0
def Or(line):
    reg2 = line[10:13]
    reg3 = line[13:16]
    reg1 = line[7:10]

    string = ""

    for i in range(0,16):
        string += (registers[reg2][i] or registers[reg3][i])
    registers[reg1] = string


def And(line):
    reg2 = line[10:13]
    reg3 = line[13:16]
    reg1 = line[7:10]

    string = ""

    for i in range(0,16):
        string += (registers[reg2][i] and registers[reg3][i])
    registers[reg1] = string

def xor(line):
    reg2 = line[10:13]
    reg3 = line[13:16]
    reg1 = line[7:10]

    string = ""

    for i in range(0,16):
        if (registers[reg2][i] == registers[reg3][i]):
            string += '0'
        else :
            string += '1'
    registers[reg1] = string


def left_shift(line):
    reg = line[5:8]
    shift_value = convert_to_decimal(line[8:16])
    value = registers[reg]
    if (shift_value <= 16):
        value = value[shift_value:]
        value += (16-len(value))*'0'
        registers[reg] = value
    else:
        registers[reg] = '0'*16
        #overflow ?



def right_shift(line):
    reg = line[5:8]
    shift_value = convert_to_decimal(line[8:16])
    value = registers[reg]
    if (shift_value <= 16):
        value2 = value[:len(value) -shift_value]
        value = (16-len(value2))*'0' + value2
        registers[reg] = value
    else:
        registers[reg] = '0'*16
        #overflow ?

def divide(line):
    reg1 = line[10:13]
    reg2 = line[13:16]

    quotient = convert_to_decimal(registers[reg1])//convert_to_decimal(registers[reg2])
    remainder =  convert_to_decimal(registers[reg1])%convert_to_decimal(registers[reg2])
    quotient = convert_to_binary(quotient)
    quotient = (16-len(quotient))*'0' + quotient
    remainder = convert_to_binary(remainder)
    quotient = (16-len(remainder))*'0' + remainder

    registers['000'] = quotient
    registers['001'] = remainder


def invert(line):
    reg1 = line[10:13]
    reg2 = line[13:16]

    string = ""

    for i in registers[reg2]:
        if (i == '0'):
            string+= '1'
        else :
            string += '0'
    registers[reg1] = string


def store(line):
    global memory_addresses
    reg = line[5:8]
    memory = line[8:16]
    
    variables[memory] = registers[reg]

def load(line):
    global memory_addresses
    reg = line[5:8]
    memory = line[8:16]
    
    registers[reg] = variables[memory]

def compare(line):
    global flag_reset

    reg1 = line[10:13]
    reg2 = line[13:16]
    val1 = convert_to_decimal(registers[reg1])
    val2 = convert_to_decimal(registers[reg2])
    print(val1,val2)
    flag = registers['111']

    if (val1 == val2):
        flag = flag[:15] + '1'
        registers['111'] = flag
        

    elif (val1 > val2):
        flag = flag[:14] + '1' + flag[15]
        registers['111'] = flag

    else:
        flag = flag[:13] + '1' + flag[14:16] 
        registers['111'] = flag

    flag_reset = 1


def jump(line1):
        
    global contd
    global program_counter                                #to use as local program counter
    mem_address= convert_to_decimal( line1[8:16])         #mem_address as a line number
    
    binaryy = open("binary.txt",'r')

    binary2 = open("binary2.txt", 'w')

    program_counter=0                                       #PC reset

    for line in binaryy.readlines():                        #re reads the file binary file
        program_counter+=1                                  #PC incremented
        if mem_address >= program_counter:                  #ignores lines before the mem_address
            continue
        elif mem_address < contd:                           #checks if the mem address is before the present execution line
            if program_counter <= contd :                   #while local c is < global PC
                command = line[0:5]
                category = instructions[command]
                output(category, line)
                binary2.write(line)
                
        elif mem_address > contd:                           #checks if the mem address is after the present execution line
            command = line[0:5]                             #simply the rest of the code is executed
            category = instructions[command]
            output(category, line)
            binary2.write(line)
        
    binaryy.close()
    binary2.close()
    
def graph_bonus(memory_addresses):
    cycles=range(1,len(memory_addresses)+1)
    plt.scatter(cycles,memory_addresses)
    plt.xlabel("Cycle")
    plt.ylabel("Memory Address")
    plt.show()

if (__name__ == '__main__'):
    input()
    process()
    memory_dump()
    graph_bonus(memory_addresses)        
