
import os
from sys import stdin, stdout
Isa= open("isa.txt",'w') # opening text file containing assembly code
binary= open("binary.txt",'w')# writing output into this file
'''
instructions is a dict storing op codes and binary codes
types is storing op code and instruction type
registers is mapping register name to address
used_instr keeps track of which opcodes were used or attempted to use
variables stores any var declarations
error msg is a string that prints out the error
'''
def label_check(line,iteration):
    words= line.split()
    global error_msg
    global linecount
    
    #LABELS
    #checking for label to remove the label and move ahead with the instruction following the label name
    if (":" in words):  #to check for wrong label naming 
        error_msg+="Improper label naming: no spaces allowed between label name and colon(:) at line no"+str(linecount)
        return False
     
    elif (":" == words[0][len(words[0])-1]):  #to check for the presence of a label
        
        c=0
        for i in words[0][:len(words[0]) -1]:
            if ( i.isalnum() or i== "_"):    #to check if label is made of alphabets numbers and underscores
                c+=1
          
        if c== len(words[0]) -1:  #checks if all characters are valid    
            if(iteration == 0): 
                if words[0] not in variables:  #checks if label name already a variable
                    if (words[0] not in labels ): 
                        #checks for duplicacy
                        if (iteration == 0):
                            labels.append(words[0][:-1])
                            
                            words= words[1:]
                        return True
                        #here, once the label name is verified, the rest of the words are re defined as words
                        #this lets the rest of the program to check the instructions for correctness
                        
                    else:  
                        error_msg+= "Label already defined at line no"+str(linecount)
                        return False 
                else: 
                    error_msg+= "Misuse of variables as labels at line no"+str(linecount)
                    return False
            else:
                return True
        else : 
            error_msg+= "Label name contains characters other than of alphanumeric characters and underscores at line no"+str(linecount)    
            return False
                
        if len(words)== 0: #checks if an instruction is followed by the name or not
            error_msg+="Label not followed by an instruction at line no"  +str(linecount)
            return False
  

def registerNaming (type, line):
    global linecount
    list= line.split()
    c=0
    global error_msg
    for i in list[1:]:
        if i in registers:
            c+=1
    if c!= registerNumber[type]:
        error_msg+= "Typos in register name at line no"+str(linecount)
        return False
    return True


def convert_to_binary(a):
    stri = ""
    while(a>0):
        stri += str(a%2)
        a = a//2
    return stri[::-1]

def passone():
    global error_msg
    global ex
    global line_number
    global label_line
    try:
        hlt_flag = False
       
        for line in stdin:
            if (("var" not in line) and (len(line) >0) ):
                line_number+=1
            if (':' in line ):
                if(label_check(line,0)):
                    words = line.split()
                    label_line[words[0][:len(words[0])-1]]=line_number-1
            Isa.write(line)
            if (hlt_flag):
                if (line == "\n"):
                    Isa.close()
                    break
                else :
                    
                    error_msg+= "hlt instruction is not the last instruction\n"
                    ex = 1
                    Isa.close()
                    break
    
        
            if ("hlt" in line.strip()):
                
                hlt_flag = True
    except EOFError:
         Isa.close() 
        
        
    
    
    

instructions = {"hlt":"10011","je":'10010',"jgt":'10001',"jlt":'10000',"jmp":'01111',"cmp":'01110',"not":'01101',"mul":'00110',"div":'00111',"rs":'01000',"ls":'01001',"xor":'01010',"or":'01011',"and":'01100',"add":'00000',"sub":'00001',"mov":'00010',"ld":'00100',"st":'00101'}
types = {"hlt":"F","je":'E',"jgt":'E',"jlt":'E',"jmp":'E',"cmp":'C',"not":'C',"mul":'A',"div":'C',"rs":'B',"ls":'B',"xor":'A',"or":'A',"and":'A',"add":'A',"sub":'A',"mov":'B',"ld":'D',"st":'D'}
registers={'R0':"000",'R1':"001",'R2':"010",'R3':"011",'R4':"100",'R5':"101",'R6':"110",'flags':"111"}
registerNumber  = {"A": 3, "B": 1, "C": 2, "D": 1, "E": 0, "F": 0 }

used_instr=[]
variables=[]
labels= []
error_msg=""
mov_overload = 0
line_number = 0
linecount=0
ex = 0
label_line = {}
flag_spot = 0

# most print commands here are debug statements
passone()

Isa = open("isa.txt",'r')
for line in Isa.readlines():
    mov_overload = 0
    flag_spot = 0
    
    linecount+=1
    words= line.split()
    
    
    #LABELS
    #checking for label to remove the label and move ahead with the instruction following the label name
    # if (label_check(line,1)):
    #    words = words[1:]

    # if (error_msg != ""):   #or else: gives the returned value as false; that implies error_msg== ""
    #     break
    
    
    #if no errors are encountered, the rest of the words are now checked for the instructions         
      
    
    #INSTRUCTIONS
    if (words[0] in instructions):#if the 1st element in input belongs to the set of keys of instructions ie the valid opcodes
        used_instr.append(words[0])# add to used instr
        
        opcode = instructions.get(words[0])#get binary value of instruction
        instr_type = types.get(words[0])#get the type
        # print(opcode,instr_type)#debug statement
        
        if words[0]=="mov" :   #to keep the overloading of the two mov instructions in check
            if (words[2] in registers or words[2] == "FLAGS"):  #by default type is set as B,
                instr_type= "C"  #if the 3rd word is a register, type is redefined as C
                mov_overload = 1
                if (words[2] == "FLAGS"):
                    flag_spot =1
                
        if(registerNaming(instr_type, line)):
            continue
        elif (error_msg!=""):
            break
        
        if instr_type=='C':
            if(len(words)==3):# the expected length for this instruction type
                reg1 = registers.get(words[1])# the second statement should have reg1
                reg2 = registers.get(words[2])
                if mov_overload == 1:
                    opcode = '00011'
                # print(reg1)
                # print(reg2)
                if(flag_spot == 1):
                        reg2 = "111"
                if ((len(reg1) and len(reg2))==3):# checking whether register naming was correct or not, for some reason the len is 3 not 2 
                    
                    binary_code= opcode+('0'*5)+reg1+reg2+"\n"
                    binary.write(binary_code)
                else:
                    error_msg+="Invalid Register naming at "+str(linecount)
                    break
            else:
                error_msg+="Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                break
        # similar to the above one the following 2 types follow the same pattern
        elif (instr_type=='B'):
            if(len(words)==3):  
                reg = registers.get(words[1])# storing the memory address
                if (words[2][0] == '$'):
                    immediate = words[2]
                    
                    immediate = int(immediate[1:])
                elif(words[2] in variables):
                    immediate = variables[words[2]]
                
                else:
                    error_msg += "Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                    
                    break
               
                
                if(immediate<=255):
                    
                    binary_code=opcode+reg+((8-len(convert_to_binary(immediate)))*'0')+convert_to_binary(immediate)+"\n"
                    

                    binary.write(binary_code)
                else:
                    immediate = convert_to_binary(immediate)
                    immediate = immediate[-9:-1]
                    binary_code = opcode + reg + immediate + "\n"
                    binary.write(binary_code)
                    
            else:
                error_msg+="Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                break
        elif (instr_type == 'D'):
            
            if(len(words) == 3):
                
                reg = registers.get(words[1])
                # print(words[2])
                # print(variables)
                if (words[2] in variables):
                    memory = convert_to_binary(line_number)
                    binary_code = opcode + reg+(8-len(memory))*'0' + memory + '\n'
                    binary.write(binary_code)
                    line_number+=1
                elif(len(words[2]) == 8):
                    binary_code = opcode + reg + words[2] + '\n'
                    binary.write(binary_code)
                    
            else:
                error_msg += "Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                break
        elif instr_type=='A':
            if(len(words)==4):  
                reg1 = registers.get(words[1])# storing the memory address
                reg2 = registers.get(words[2])
                reg3 = registers.get(words[3])
                
                
                if(True):
                    
                    binary_code=opcode+"00"+reg1+reg2+reg3+"\n"
                    # print(binary_code)
                    binary.write(binary_code)
                else:
                    error_msg+="Syntax Error\n"
                    break
            else:
                error_msg+="Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                break
        elif instr_type=='E':
            if(len(words)==2):  
                mem_address = words[1]# storing the memory address
                
                if (words[1] in labels):
                    mem_address= (convert_to_binary(label_line[words[1]]))
                    mem_address = (8-len(mem_address))*'0' + mem_address

                else :
                    continue
                    #print("fail")
                if(len(mem_address)==8):
                    binary_code=opcode+("0"*3)+mem_address+"\n"
                    binary.write(binary_code)
                else:
                    error_msg+="Syntax Error\n"
                    break
            else:
                error_msg+="Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                break
        elif instr_type=="F":
            if(len(words)==1):
                binary_code= opcode+("0"*11)+"\n"
                binary.write(binary_code)
                break
            else:
                error_msg+="Invalid Syntax for " + words[0] +"at line no"+ linecount+"\n"
                break
        if opcode==None:
            error_msg+="invalid instruction name\n"
            break
            
# now if the above code doesn't run then its either a variable declaration or typo in instruction name
    elif (words[0]=='var' and len(used_instr)==0):# len(used_instr) ensures that no other instr was used before a var declaration
        c = 0
        for i in words[1]:
            if (i.isalnum() or i == '_'):
                c+=1
        if (c == len(words[1])):
            
            variables.append(words[1])
        else:
            error_msg+="Improper variable naming at line no" +str(linecount)
            break
    elif(words[0]=='var' and len(used_instr)>0):
        error_msg+="variables not declared at the top"
        break
    elif(words[0] not in instructions):
        error_msg+="Typo in instruction name at line no "+ str(linecount)
        break
# hlt error check is done at the end, assuming there are no error msg's prior to this halt errors are the only one left    
if(error_msg==""):   
    if("hlt" not in used_instr):# if halt was never called
        error_msg+="hlt instruction is not used\n"
    elif ("hlt" in used_instr): # halt was called but was not the last one to be called
        if (used_instr.index("hlt")!= len(used_instr)-1):
                
                error_msg+= "hlt instruction is not the last instruction at line no"+linecount+"\n"
binary.write(error_msg)
binary.close()
Isa.close()

binary = open("binary.txt",'r+')
for line in binary.readlines():
    print(line,end="")
binary.close()
#print(label_line)



#     cmp R4 R6
# jmp 10001000
# hlt

    
