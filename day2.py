#!/usr/bin/env python3

# 1 - Add 2 Ints, store result (2 numbers after this opcode are indices/positions)
# 2 - Mul. 2 Ints
# 99 - Finished/Halt

def run_process(p):
    i = 0
    while i <= len(p):
        op = p[i]
        #print(op)
        if op == 1:
            #print("Add")
            arg1 = p[p[i+1]]
            arg2 = p[p[i+2]]
            result = arg1 + arg2
            p[p[i+3]] = result
            i += 4
            continue
        if op == 2:
            #print("Mult")
            arg1 = p[p[i+1]]
            arg2 = p[p[i+2]]
            result = arg1 * arg2
            p[p[i+3]] = result
            i += 4
            continue
        if op == 99:
            #print("Halt")
            break
        else:
            #print("Invalid operation")
            break
    return p

program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,10,19,23,2,9,23,27,1,6,27,31,2,31,9,35,1,5,35,39,1,10,39,43,1,10,43,47,2,13,47,51,1,10,51,55,2,55,10,59,1,9,59,63,2,6,63,67,1,5,67,71,1,71,5,75,1,5,75,79,2,79,13,83,1,83,5,87,2,6,87,91,1,5,91,95,1,95,9,99,1,99,6,103,1,103,13,107,1,107,5,111,2,111,13,115,1,115,6,119,1,6,119,123,2,123,13,127,1,10,127,131,1,131,2,135,1,135,5,0,99,2,14,0,0]

# part 1
process = list(program)
process[1] = 12
process[2] = 2
process = run_process(process)
print(f"Result: {process[0]}")

# part 2
target = 19690720
for x in range(100):
    for y in range(100):
        process = list(program)
        process[1] = x
        process[2] = y
        process = run_process(process)
        result = process[0]
        if result == target:
            print(f"Success x={x}, y={y} => {target}")
            print(f"Answer: {x*100+y}")
            exit(0)


