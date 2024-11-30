from importlib import import_module
from sys import argv


def main():
    if len(argv) not in (2, 3):
        print('Usage: aoc <problem_no> [<part>]')
        exit(1)
    try:
        puzzle_no = int(argv[1])
    except ValueError:
        print(f'Invalid problem number {argv[1]}')
        exit(1)
    if not 1 <= puzzle_no <= 25:
        print(f'Invalid problem number {puzzle_no}')
    if len(argv) == 3:
        try:
            part = int(argv[2])
        except ValueError:
            print(f'Invalid part {argv[2]}')
        if part not in (1, 2):
            print(f'Invalid part {part}')
        parts = (part,)
    else:
        parts = (1, 2)

    puzzle = import_module(f'puzzle{puzzle_no:0>2d}')
    
    print(puzzle.__name__)
    if 1 in parts:
        print('Part 1:')
        print(puzzle.part_1())
        print()
    if 2 in parts:
        print('Part 2:')
        print(puzzle.part_2())
        print()


if __name__ == '__main__':
    main()
