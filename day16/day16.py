from typing import List, Iterator
import itertools

def pattern(output_element: int) -> Iterator[int]:
   while True:
        for _ in range(output_element):
           yield 0
        for _ in range(output_element):
           yield 1
        for _ in range(output_element):
           yield 0
        for _ in range(output_element):
           yield -1

def ones_digit(n: int) -> int:
    if n > 0:
        return n % 10
    else:
        return (-n) % 10

def fft_phase(numbers: List[int]) -> List[int]:
    output = []
    n = len(numbers)
    for i in range(n):
        pat = pattern(i + 1)
        next(pat)
        
        values = list(zip(pat, numbers))
        #print(values)
        total = sum(p * n for p, n in values)
        #print(total)
        output.append(ones_digit(total))
    return output

offset = 5971981
raw = "59719811742386712072322509550573967421647565332667367184388997335292349852954113343804787102604664096288440135472284308373326245877593956199225516071210882728614292871131765110416999817460140955856338830118060988497097324334962543389288979535054141495171461720836525090700092901849537843081841755954360811618153200442803197286399570023355821961989595705705045742262477597293974158696594795118783767300148414702347570064139665680516053143032825288231685962359393267461932384683218413483205671636464298057303588424278653449749781937014234119757220011471950196190313903906218080178644004164122665292870495547666700781057929319060171363468213087408071790"
numbers = [int(c) for c in raw]
mega = numbers * 10_000


# for _ in range(100):
#     numbers = fft_phase(numbers)
# print(numbers[:8])


# now repeated 10000 times
# so 6 million numbers long
# each phase is 6 million * 6 million, which is too much

# we only want 8 specific digits

# 0, -1, 0, 1, 0, -1, 0, 1
# s[3] + s[7] + s[11] + ... - s[1] - s[5] - ...

# 1, 0, 0, -1, -1, 0, 0, 1, 1, 0, 0, -1, -1
# s[0] + s[7] + s[8] + s[15] + s[16] + ....
#      - s[3] - s[4] - s[10] - s[11] - ....

### part 2

def part2(raw: str) -> List[int]:
    offset = int(raw[:7])
    numbers = [int(c) for c in raw] * 10_000

    assert offset > len(numbers) // 2

    # pattern is tail([0] * n, [1] * n, [0] * n, [-1] * n)
    # in particular, pattern is 0 up until place n
    # in particular, if n >= len(numbers) // 2, pattern is just 1 starting at n until the end

    # that means we only need to sum up until the end
    for _ in range(100):

        # last position
        pos = len(numbers) - 1
        total = 0

        while pos >= offset:
            total += numbers[pos]
            numbers[pos] = ones_digit(total)
            pos -= 1


    return numbers[offset:offset+8]

