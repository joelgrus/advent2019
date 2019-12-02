from typing import List

Program = List[int]

def run(program: Program) -> None:
    pos = 0
    
    while program[pos] != 99:  # halt
        opcode, loc1, loc2, loc3 = program[pos], program[pos + 1], program[pos + 2], program[pos + 3]
        if opcode == 1:
            program[loc3] = program[loc1] + program[loc2]
        elif opcode == 2:
            program[loc3] = program[loc1] * program[loc2]
        else:
            raise RuntimeError(f"invalid opcode: {program[pos]}")
        
        pos += 4

prog1 = [1,0,0,0,99]; run(prog1); assert prog1 == [2,0,0,0,99]
prog2 = [2,3,0,3,99]; run(prog2); assert prog2 == [2,3,0,6,99]
prog3 = [2,4,4,5,99,0]; run(prog3); assert prog3 == [2,4,4,5,99,9801]
prog4 = [1,1,1,4,99,5,6,0,99]; run(prog4); assert prog4 == [30,1,1,4,2,5,6,0,99]

def alarm(program: Program, noun: int = 12, verb: int = 2) -> int:
    program = program[:]
    program[1] = noun
    program[2] = verb
    run(program)
    return program[0]

PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,5,23,2,10,23,27,2,27,13,31,1,10,31,35,1,35,9,39,2,39,13,43,1,43,5,47,1,47,6,51,2,6,51,55,1,5,55,59,2,9,59,63,2,6,63,67,1,13,67,71,1,9,71,75,2,13,75,79,1,79,10,83,2,83,9,87,1,5,87,91,2,91,6,95,2,13,95,99,1,99,5,103,1,103,2,107,1,107,10,0,99,2,0,14,0]

# print(alarm(PROGRAM))

TARGET = 19690720

for noun in range(100):
    for verb in range(100):
        output = alarm(PROGRAM, noun, verb)
        if output == TARGET:
            print(noun, verb, 100 * noun + verb)
            break