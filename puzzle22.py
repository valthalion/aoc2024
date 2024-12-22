from collections import defaultdict, deque


testing = False
MODULO = 16777216


def read_data():
    with open(f'puzzle22-test{testing}.in' if testing else 'puzzle22.in', 'r') as f:
        for line in f:
            yield int(line.strip())


def prng(seed, count=2000):
    value = seed
    for _ in range(count):
        value = (value ^ (value << 6)) % MODULO
        value = (value ^ (value >> 5)) % MODULO
        value = (value ^ (value << 11)) % MODULO
        yield value


def last(seq):
    for result in seq:
        pass
    return result


def bananas(seed):
    results = {}
    group = deque(maxlen=4)
    last_price = seed % 10
    gen = prng(seed)

    for new_value in (next(gen), next(gen), next(gen)):
        new_price = new_value % 10
        group.append(new_price - last_price)
        last_price = new_price

    for new_value in gen:
        new_price = new_value % 10
        group.append(new_price - last_price)
        diff_seq = tuple(group)
        if diff_seq in results:
            pass  # only first time the diff_seq is seen can be used
        else:
            results[diff_seq] = new_price
        last_price = new_price

    return results


def merge(results_dicts):
    total = defaultdict(int)
    for results in results_dicts:
        for diff_seq, num_bananas in results.items():
            total[diff_seq] += num_bananas
    return total


def part_1():
    return sum(last(prng(seed)) for seed in read_data())


def part_2():
    seeds = read_data()
    banana_counts = (bananas(seed) for seed in seeds)
    total_bananas = merge(banana_counts)
    return max(total_bananas.values())
