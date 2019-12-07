#!/usr/bin/env python3

# parameter/immediate mode is indirect vs immedaite adressing
# opcode is always 2 digits
# numbers can be longer, format will be: modes, opcode
def read_arg(p, pc, mode):
    arg = None
    if mode == 0:
        arg = p[p[pc]]
        print(f" > Read: {arg} at pos {p[pc]} in mode {mode}")
    else:
        arg = p[pc]
        print(f" > Read: {arg} at pos {pc} in mode {mode}")    
    return pc+1, arg


def write_arg(p, pc, val, mode):
    if mode == 0:        
        p[p[pc]] = val
        print(f" > Write: {val} to pos {p[pc]} in mode {mode}")
    else:
        p[pc] = val
        print(f" > Write: {val} to pos {pc} in mode {mode}")
    return pc+1


def take(p, pc, num, mode):
    args = []
    for i in range(num):
        pc, arg = read_arg(p, pc, mode[i])
        args.append(arg)
    return pc, args


def run_process(p):
    pc = 0x0    
    while pc <= len(p):     
        #print(f"{p} ({len(p)})")   
        print(f"PC @ {hex(pc)}")
        mode = [0,0,0]
        digits = list(str(p[pc]))
        print(f" - Op: {digits}")
        digits.reverse()
        l = len(digits)
        op = -1
        if l == 1:
            op = int(digits[0])
        elif l >= 2:
            op = int(str(digits[1])+str(digits[0]))
        if l >= 3:
            mode[0] = int(digits[2])
        if l >= 4:
            mode[1] = int(digits[3])
        if l >= 5:
            mode[2] = int(digits[4])
        print(f" - Opcode: {op}")
        # every opcode has length 1 (as in takes one spot in the program array)
        pc += 1
        print(f" - Mode: {mode}")
        if op == 1: #add
            pc, args = take(p, pc, 2, mode)
            result = args[0] + args[1]
            print(f" - Add {args[0]},{args[1]} -> {result}")
            pc = write_arg(p, pc, result, mode[2])
        elif op == 2: #mul
            pc, args = take(p, pc, 2, mode)
            result = args[0] * args[1]
            print(f" - Mul {args[0]},{args[1]} -> {result}")
            pc = write_arg(p, pc, result, mode[2])
        elif op == 3: # store input
            inp = int(input()) # unsafe
            pc = write_arg(p, pc, inp, 0)
        elif op == 4: # output
            pc, args = take(p, pc, 1, mode)
            print(f" - Out: {args[0]}")            
        elif op == 5: # jump if true
            pc, args = take(p, pc, 2, mode)
            if args[0] != 0:
                pc = args[1]
                print(f" - jtrue taken {hex(args[0])}")
            else:
                print(" - jtrue not taken")
        elif op == 6: # jump if false
            pc, args = take(p, pc, 2, mode)
            if args[0] == 0:
                pc = args[1]
                print(f" - jfalse taken {hex(args[0])}")
            else:
                print(" - jfalse not taken")
        elif op == 7: # less than
            pc, args = take(p, pc, 2, mode)
            result = 0
            store = 0
            if args[0] < args[1]:
                store = 1 
                print(f" - cmplt: {args[0]},{args[1]}")
            pc = write_arg(p, pc, store, mode[2])
        elif op == 8: # equals
            pc, args = take(p, pc, 2, mode)
            store = 0
            if args[0] == args[1]:
                store = 1 
                print(f" - cmpeq: {args[0]},{args[1]}")
            pc = write_arg(p, pc, store, mode[2])
        elif op == 99: # halt
            break
        else:
            print("Invalid operation")
            break  
    return p

#program = [1101,100,-1,4,0]
program  = [3,225,1,225,6,6,1100,1,238,225,104,0,1102,9,19,225,1,136,139,224,101,-17,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,2,218,213,224,1001,224,-4560,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,25,63,224,101,-1575,224,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1102,55,31,225,1101,38,15,225,1001,13,88,224,1001,224,-97,224,4,224,102,8,223,223,101,5,224,224,1,224,223,223,1002,87,88,224,101,-3344,224,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1102,39,10,225,1102,7,70,225,1101,19,47,224,101,-66,224,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,1102,49,72,225,102,77,166,224,101,-5544,224,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,101,32,83,224,101,-87,224,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,80,5,225,1101,47,57,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,107,226,677,224,1002,223,2,223,1006,224,344,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,359,1001,223,1,223,8,677,226,224,102,2,223,223,1005,224,374,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,404,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,419,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,434,101,1,223,223,8,226,677,224,1002,223,2,223,1006,224,449,101,1,223,223,1007,677,226,224,102,2,223,223,1005,224,464,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,494,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,509,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,524,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,539,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,554,101,1,223,223,7,226,677,224,102,2,223,223,1005,224,569,101,1,223,223,1108,677,226,224,1002,223,2,223,1005,224,584,101,1,223,223,108,677,677,224,1002,223,2,223,1006,224,599,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,614,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,644,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,674,1001,223,1,223,4,223,99,226]
#program = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
#program = [3,9,8,9,10,9,4,9,99,-1,8]
# 13787043
# 3892695
process = list(program)
process = run_process(process)


