from sys import stdin

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
    binary = open("binary.txt",'r')
    for line in binary.readlines():
        command = line[0:6]
        category = instructions[command]


    

if (__name__ == '__main__'):
    input()
    process()
    memory_dump()
        