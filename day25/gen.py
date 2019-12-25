items = [
    'easter egg',
    'mug',
    'sand',
    'weather machine',
    'festive hat',
    'shell',
    'whirled peas',
    'space heater'
]

def make_command(sset):
    drops = [f"drop {item}" for item in items]
    takes = [f"take {item}" for item in sset]
    south = ["south"]

    return "\n".join(drops + takes + south)

for x in range(2 ** 8):
    sset = {item for i, item in enumerate(items) if x >> i & 1}
    print(make_command(sset))
    input()

