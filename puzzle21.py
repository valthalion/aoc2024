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
            return f'{v * abs(vert)}{h * abs(horiz)}A'
        return f'{h * abs(horiz)}{v * abs(vert)}A'
    else:
        if pos.real == -2 and pos.imag + vert == 0:
            return f'{h * abs(horiz)}{v * abs(vert)}A'
        return f'{v * abs(vert)}{h * abs(horiz)}A'


def read_data():
    with open(f'puzzle21{"-test" if testing else ""}.in', 'r') as f:
        for line in f:
            yield line.strip()


@cached
def calculate_len(button, prev, num_keyboards):
    if num_keyboards == 0:
        return 1  # direct push
    return process(translate(buttons[prev], buttons[button]), num_keyboards=num_keyboards - 1)


def process(seq, start='A', num_keyboards=3):
    if num_keyboards == 0:
        return len(seq)
    seq_len, pos = 0, 'A'
    for button in seq:
        seq_len += calculate_len(button, pos, num_keyboards)
        pos = button
    return seq_len


def complexity(code, seq_len):
    return seq_len * int(code[:-1])


def part_1():
    codes = list(read_data())
    seq_lens = (process(code) for code in codes)
    return sum(complexity(code, seq_len) for code, seq_len in zip(codes, seq_lens))


def part_2():
    codes = list(read_data())
    seq_lens = (process(code, num_keyboards=26) for code in codes)
    return sum(complexity(code, seq_len) for code, seq_len in zip(codes, seq_lens))
