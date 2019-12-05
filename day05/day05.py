from typing import List, NamedTuple, Tuple

def parse_opcode(opcode: int) -> Tuple[int, List[int]]:
    opcode_part = opcode % 100

    hundreds_digit = (opcode // 100) % 10
    thousands_digit = (opcode // 1000) % 10
    ten_thousands_digit = (opcode // 10000) % 10

    return opcode_part, [hundreds_digit, thousands_digit, ten_thousands_digit]

# 1 is immediate mode, 0 is position mode

Program = List[int]

def run(program: Program, input: List[int]) -> List[int]:
    program = program[:]
    output = []

    pos = 0

    while program[pos] != 99:  # halt
        opcode, modes = parse_opcode(program[pos])
        print(pos, opcode, modes)

        if opcode == 1:
            # Add
            if modes[0] == 0:
                value1 = program[program[pos + 1]]
                print(f"loc1 is {program[pos + 1]} so value1 is {value1}")
            else:
                value1 = program[pos + 1]
                print(f"value1 is immediate {value1}")

            if modes[1] == 0:
                value2 = program[program[pos + 2]]
                print(f"loc2 is {program[pos + 2]} so value2 is {value2}")
            else:
                value2 = program[pos + 2]
                print(f"value2 is immediate {value2}")

            print("adding", value1, "and", value2, "and sticking the result at", program[pos+3])

            program[program[pos + 3]] = value1 + value2
            pos += 4
        elif opcode == 2:
            # Multiply
            if modes[0] == 0:
                value1 = program[program[pos + 1]]
                print(f"loc1 is {program[pos + 1]} so value1 is {value1}")
            else:
                value1 = program[pos + 1]
                print(f"value1 is immediate {value1}")

            if modes[1] == 0:
                value2 = program[program[pos + 2]]
                print(f"loc2 is {program[pos + 2]} so value2 is {value2}")
            else:
                value2 = program[pos + 2]
                print(f"value2 is immediate {value2}")

            print("multiplying", value1, "and", value2, "and sticking the result at", program[pos+3])


            program[program[pos + 3]] = value1 * value2
            pos += 4
        elif opcode == 3:
            # Get input and store at location
            loc = program[pos + 1]
            input_value = input[0]
            input = input[1:]
            program[loc] = input_value
            pos += 2
        elif opcode == 4:
            # Get output from location
            if modes[0] == 0:
                loc = program[pos + 1]
                value = program[loc]
            else:
                value = program[pos + 1]

            output.append(value)
            pos += 2

        elif opcode == 5:
            # jump if true
            if modes[0] == 0:
                value1 = program[program[pos + 1]]
                print(f"loc1 is {program[pos + 1]} so value1 is {value1}")
            else:
                value1 = program[pos + 1]
                print(f"value1 is immediate {value1}")

            if modes[1] == 0:
                value2 = program[program[pos + 2]]
                print(f"loc2 is {program[pos + 2]} so value2 is {value2}")
            else:
                value2 = program[pos + 2]
                print(f"value2 is immediate {value2}")

            if value1 != 0:
                pos = value2
            else:
                pos += 3

        elif opcode == 6:
            # jump if false
            if modes[0] == 0:
                value1 = program[program[pos + 1]]
                print(f"loc1 is {program[pos + 1]} so value1 is {value1}")
            else:
                value1 = program[pos + 1]
                print(f"value1 is immediate {value1}")

            if modes[1] == 0:
                value2 = program[program[pos + 2]]
                print(f"loc2 is {program[pos + 2]} so value2 is {value2}")
            else:
                value2 = program[pos + 2]
                print(f"value2 is immediate {value2}")

            if value1 == 0:
                pos = value2
            else:
                pos += 3

        elif opcode == 7:
            # less than
            if modes[0] == 0:
                value1 = program[program[pos + 1]]
                print(f"loc1 is {program[pos + 1]} so value1 is {value1}")
            else:
                value1 = program[pos + 1]
                print(f"value1 is immediate {value1}")

            if modes[1] == 0:
                value2 = program[program[pos + 2]]
                print(f"loc2 is {program[pos + 2]} so value2 is {value2}")
            else:
                value2 = program[pos + 2]
                print(f"value2 is immediate {value2}")

            if value1 < value2:
                program[program[pos + 3]] = 1
            else:
                program[program[pos + 3]] = 0
            pos += 4


        elif opcode == 8:
            # equals
            if modes[0] == 0:
                value1 = program[program[pos + 1]]
                print(f"loc1 is {program[pos + 1]} so value1 is {value1}")
            else:
                value1 = program[pos + 1]
                print(f"value1 is immediate {value1}")

            if modes[1] == 0:
                value2 = program[program[pos + 2]]
                print(f"loc2 is {program[pos + 2]} so value2 is {value2}")
            else:
                value2 = program[pos + 2]
                print(f"value2 is immediate {value2}")

            if value1 == value2:
                program[program[pos + 3]] = 1
            else:
                program[program[pos + 3]] = 0
            pos += 4

        else:
            raise RuntimeError(f"invalid opcode: {opcode}")

    return output

PROGRAM = [3,225,1,225,6,6,1100,1,238,225,104,0,1002,43,69,224,101,-483,224,224,4,224,1002,223,8,223,1001,224,5,224,1,224,223,223,1101,67,60,225,1102,5,59,225,1101,7,16,225,1102,49,72,225,101,93,39,224,101,-98,224,224,4,224,102,8,223,223,1001,224,6,224,1,224,223,223,1102,35,82,225,2,166,36,224,101,-4260,224,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,102,66,48,224,1001,224,-4752,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1001,73,20,224,1001,224,-55,224,4,224,102,8,223,223,101,7,224,224,1,223,224,223,1102,18,41,224,1001,224,-738,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1101,68,71,225,1102,5,66,225,1101,27,5,225,1101,54,63,224,1001,224,-117,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1,170,174,224,101,-71,224,224,4,224,1002,223,8,223,1001,224,4,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1007,226,226,224,1002,223,2,223,1006,224,329,1001,223,1,223,1007,226,677,224,102,2,223,223,1006,224,344,1001,223,1,223,108,677,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,8,677,226,224,1002,223,2,223,1006,224,389,101,1,223,223,7,226,226,224,1002,223,2,223,1005,224,404,101,1,223,223,7,677,226,224,102,2,223,223,1005,224,419,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1008,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,7,226,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,479,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,494,101,1,223,223,8,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,524,1001,223,1,223,1107,226,226,224,102,2,223,223,1005,224,539,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,554,101,1,223,223,107,226,677,224,102,2,223,223,1005,224,569,1001,223,1,223,1108,226,677,224,1002,223,2,223,1005,224,584,1001,223,1,223,1107,226,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,614,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1008,677,677,224,1002,223,2,223,1006,224,644,101,1,223,223,107,677,677,224,1002,223,2,223,1005,224,659,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]
