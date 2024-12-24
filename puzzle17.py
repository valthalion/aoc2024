testing = False
debugging = False


def read_data():
    registers = {}
    with open(f'puzzle17{"-test" if testing else ""}.in', 'r') as f:
        registers['a'] = int(next(f).split(': ')[1])
        registers['b'] = int(next(f).split(': ')[1])
        registers['c'] = int(next(f).split(': ')[1])
        next(f)
        code = [int(n) for n in next(f).strip().split(': ')[1].split(',')]
    return registers, code


class Computer:
    def __init__(self, registers=None):
        self.registers = {'a': 0, 'b': 0, 'c': 0}
        if registers is not None:
            self.update_registers(**registers)
        self.code = None
        self.ip = None
        self.ops = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]

    def update_registers(self, **kwargs):
        self.registers.update(kwargs)

    def run(self, code):
        self.code = code
        self.ip = 0
        while self.ip < len(self.code):
            opcode, arg = self.code[self.ip : self.ip + 2]
            self.ip += 2
            if debugging: print(self.ops[opcode].__name__, arg, self.registers)
            output = self.ops[opcode](arg)
            if output is not None:
                yield output

    def combo(self, arg):
        if 0 <= arg <= 3: return arg
        if arg == 4: return self.registers['a']
        if arg == 5: return self.registers['b']
        if arg == 6: return self.registers['c']
        if arg == 7: raise ValueError('Reserved value')
        raise ValueError('Invalid Value')

    def dv(self, arg, reg):
        self.registers[reg] = self.registers['a'] >> self.combo(arg)

    def adv(self, arg):
        self.dv(arg, 'a')

    def bdv(self, arg):
        self.dv(arg, 'b')

    def cdv(self, arg):
        self.dv(arg, 'c')

    def bxl(self, arg):
        self.registers['b'] ^= arg

    def bst(self, arg):
        self.registers['b'] = self.combo(arg) & 7

    def jnz(self, arg):
        if self.registers['a'] != 0:
            self.ip = arg

    def bxc(self, arg):
        self.registers['b'] ^= self.registers['c']

    def out(self, arg):
        if debugging: print(self.combo(arg) & 7)
        return self.combo(arg) & 7


def pseudocode():
    registers, code = read_data()
    opcodes = [
        'adv: a <- a >> combo',
        'bxl: b <- b xor arg',
        'bst: b <- combo & 7',
        'jnz: if a == 0 nop else ip <- arg',
        'bxc: b <- b xor c',
        'out: output combo',
        'bdv: b <- a >> combo',
        'cdv: c <- a >> combo'
    ]
    for idx in range(0, len(code), 2):
        op = opcodes[code[idx]]
        arg = code[idx + 1]
        arg_value = f'{arg} | {arg if arg <= 3 else "abc"[arg - 4]}'
        print(op, '  --  ', arg_value)


def find_a_value(code, idx=None, a=0):
    if idx == -1:
        return a

    start = 0
    if idx is None:
        idx = len(code) - 1
        start = 1  # first triplet cannot be 0 to ensure no termination before

    a <<= 3
    for trail_a in range(start, 8):
        new_a = a | trail_a
        b = new_a & 7
        b ^= 3
        c = (new_a >> b)
        b ^= c
        b ^= 5
        if (b & 7) != code[idx]:
            continue
        final_a = find_a_value(code, idx=idx - 1, a=new_a)
        if final_a is not None:
            return final_a
    return None


def part_1():
    registers, code = read_data()
    computer = Computer(registers)
    output = computer.run(code)
    return ','.join(str(n) for n in output)


def part_2():
    registers, code = read_data()

    a_value = find_a_value(code)
    if a_value is None:
        return

    # Comment the three lines above to run this and get the pseudocode of the program
    registers['a'] = a_value
    computer = Computer(registers)
    output = list(computer.run(code))
    if len(output) == len(code) and all(x == y for x, y in zip(code, output)):
        return a_value
