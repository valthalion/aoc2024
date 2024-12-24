from collections import deque


testing = False


def read_data():
    files, gaps, mem_pos, file_id, is_file = [], deque(), 0, 0, True
    with open(f'puzzle09{"-test" if testing else ""}.in', 'r') as f:
        for c in next(f).strip():
            value = int(c)
            if is_file:
                files.append({'id': file_id, 'pos': mem_pos, 'size': value})
                file_id += 1
                is_file = False
            else:
                if value:
                    gaps.append({'pos': mem_pos, 'size': value})
                is_file = True
            mem_pos += value
    return files, gaps


def file_checksum(file):
    return sum(pos * file['id'] for pos in range(file['pos'], file['pos'] + file['size']))


def defrag(files, gaps):
    file = files.pop()
    gap = gaps.popleft()
    compacted_files = []

    while gap['pos'] < file['pos']:
        step = min(file['size'], gap['size'])
        new_file = {'id': file['id'], 'pos': gap['pos'], 'size': step}
        compacted_files.append(new_file)
        file['size'] -= step
        if file['size'] == 0:
            file = files.pop()
        gap['size'] -= step
        gap['pos'] += step
        if gap['size'] == 0:
            gap = gaps.popleft()

    files.append(file)
    files.extend(compacted_files)


def defrag2(files, gaps):
    for file in reversed(files):
        for gap in gaps:
            if gap['pos'] > file['pos']:
                break
            if gap['size'] < file['size']:
                continue
            file['pos'] = gap['pos']
            gap['pos'] += file['size']
            gap['size'] -= file['size']


def part_1():
    files, gaps = read_data()
    defrag(files, gaps)
    return sum(file_checksum(file) for file in files)


def part_2():
    files, gaps = read_data()
    defrag2(files, gaps)
    return sum(file_checksum(file) for file in files)
