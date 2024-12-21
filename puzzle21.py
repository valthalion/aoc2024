testing = False


# Define positions for each keyboard centered aroud the 'A' button, so that the same system can
# be used for both; this also makes -2 the forbidden position in both keyboards.

buttons = {
    'A': 0,
    '0': -1, '1': -2 + 1j, '2': -1 + 1j, '3': 1j, '4': -2 + 2j, '5': -1 + 2j, '6': 2j, '7': -2 + 3j,
    '8': -1 + 3j, '9': 3j, '^': -1, '<': -2 - 1j, 'v': -1 - 1j, '>': -1j
}


def cached(f):
    cache = {}
    def inner(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return inner

@cached
def translate(pos, target):
    move = target - pos
    horiz, vert = int(move.real), int(move.imag)
    h = '>' if horiz >= 0 else '<'
    v = '^' if vert >= 0 else 'v'
    # Heuristic (taken from reddit)
    # If moving left, first move horizontally and then vertically
    # If moving right, do the opposite
    # In either case, chage tactic if it would pass through the forbidden gap
    if move.real <= 0:
        if pos.imag == 0 and pos.real + horiz == -2:
            return f'{v * abs(vert)}{h * abs(horiz)}'
        return f'{h * abs(horiz)}{v * abs(vert)}'
    else:
        if pos.real == -2 and pos.imag + vert == 0:
            f'{h * abs(horiz)}{v * abs(vert)}'
        return f'{v * abs(vert)}{h * abs(horiz)}'


def read_data():
    with open(f'puzzle21{"-test" if testing else ""}.in', 'r') as f:
        for line in f:
            yield line.strip()


def keyboard_sequence(code):
    pos = buttons['A']
    seq = []
    for c in code:
        target = buttons[c]
        seq.extend(translate(pos, target))
        seq.append('A')
        pos = target
    return ''.join(seq)


def process(code, num_keyboards=3):
    seq = code
    for _ in range(num_keyboards):
        seq = keyboard_sequence(seq)
    print(len(seq))
    return seq


def complexity(code, seq):
    return len(seq) * int(code[:-1])


def part_1():
    codes = list(read_data())
    seqs = (process(code) for code in codes)
    return sum(complexity(code, seq) for code, seq in zip(codes, seqs))


def part_2():
    codes = list(read_data())
    seqs = (process(code, num_keyboards=26) for code in codes)
    return sum(complexity(code, seq) for code, seq in zip(codes, seqs))
