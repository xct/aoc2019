#!/usr/bin/env python3
from itertools import permutations 
import time

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


def run_process(p, pc, inputs):   
    output = -1
    inputs = inputs.copy()
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
        if op == 1: # add
            pc, args = take(p, pc, 2, mode)
            result = args[0] + args[1]
            print(f" - Add {args[0]},{args[1]} -> {result}")
            pc = write_arg(p, pc, result, mode[2])
        elif op == 2: # mul
            pc, args = take(p, pc, 2, mode)
            result = args[0] * args[1]
            print(f" - Mul {args[0]},{args[1]} -> {result}")
            pc = write_arg(p, pc, result, mode[2])
        elif op == 3: # store input
            if len(inputs) == 0:
                # consumed all inputs - waiting for more
                # we subtract one to rexecute the read on reentry if this process goes to sleep
                assert output != -1
                return p, pc-1, output
            else:
                inp = inputs.pop()
                pc = write_arg(p, pc, inp, mode[0])
        elif op == 4: # output
            pc, args = take(p, pc, 1, mode)
            print(f" - Out: {args[0]}")        
            output = args[0]    
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
            exit(0)  
    assert output != -1
    return p, -1, output


program  = [3,8,1001,8,10,8,105,1,0,0,21,46,59,84,93,110,191,272,353,434,99999,3,9,101,2,9,9,102,3,9,9,1001,9,5,9,102,4,9,9,1001,9,4,9,4,9,99,3,9,101,3,9,9,102,5,9,9,4,9,99,3,9,1001,9,4,9,1002,9,2,9,101,2,9,9,102,2,9,9,1001,9,3,9,4,9,99,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,1001,9,5,9,1002,9,3,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99]
#program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
#program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

'''
amp_permutations = list(permutations(range(0, 5))) 
max_total = 0
for amps in amp_permutations:
    cur = 0
    for amp in amps:        
        inputs = [cur, amp] # pop is lifo   
        process = list(program)
        _, _, cur = run_process(process, 0, inputs)
        print(f"In: {inputs}")
        print(f"Out: {cur}")
    if cur > max_total:
        max_total = cur
        max_amps = amps
    print(f"Thruster: {cur}")
print(f"Max Thruster {max_total} with sequence {max_amps}")
'''

# Part2: Feedback mode
#program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5] 
#program = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

# Don't restart the Amplifier Controller Software on any amplifier during this process. 
amp_permutations = list(permutations(range(5, 10))) 
max_total = 0
for amps in amp_permutations:
    print(amps)
    running = {}
    cur = 0
    init = True
    done = False
    # For every permutation
    while len(running) > 0 or init:
        # For every entry in amps
        for i, amp in enumerate(amps):          
            # (re)start processes that are not running      
            if i not in running and init == True:
                # not running ? start process               
                inputs = [cur, amp]
                process = list(program) # copy
                print(f'Process {i} started at pc {hex(0)}, In: {cur}')
                process, pc, cur = run_process(process, 0, inputs)              
            else:
                # it is running? continue               
                inputs = [cur,]
                processs, pc = running[i]
                print(f'Process {i} continues at pc {hex(pc)}, In: {cur}')
                process, pc, cur = run_process(process, pc, inputs)
            # a process paused (waiting for input)
            if pc != -1:
                print(f'Process {i} paused, Out: {cur}')                
                running[i] = (process,pc)
            else:
                print(f'Process {i} ended Out: {cur}')              
                if i == 4:
                    # exit criterion, when last amp reaches halt signals
                    running = []
                    break
                else:                   
                    print(f'Warning: Termination scheduled by {i}')
                    done = True
        if done:
            print(f'Warning: Early stopping')
            time.sleep(.1)
            break
        init = False
    if cur > max_total:
        max_total = cur
        max_amps = amps
    print(f"Thrust: {cur}")
print(f"Max Thrust {max_total} with sequence {max_amps}")