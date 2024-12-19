from collections import defaultdict


testing = False


class PatternMatcher:
    def __init__(self):
        self.patterns = defaultdict(set)
        self.max_len = 0
        self._feasibility_cache = {'': True}
        self._combinations_cache = {'': 1}

    def add_pattern(self, pattern):
        pattern_len = len(pattern)
        self.patterns[pattern_len].add(pattern)
        if len(pattern) > self.max_len:
            self.max_len = len(pattern)

    def match(self, target):
        for pattern_len in range(1, max(self.max_len, len(target))):
            if (pattern := target[:pattern_len]) in self.patterns[pattern_len]:
                yield pattern

    def can_build(self, target):
        if target not in self._feasibility_cache:
            self._feasibility_cache[target] = self._can_build(target)
        return self._feasibility_cache[target]

    def _can_build(self, target):
        for match in self.match(target):
            if self.can_build(target[len(match):]):
                return True
        return False

    def combinations(self, target):
        if target not in self._combinations_cache:
            self._combinations_cache[target] = self._combinations(target)
        return self._combinations_cache[target]

    def _combinations(self, target):
        total = 0
        for match in self.match(target):
            total += self.combinations(target[len(match):])
        return total


def read_data():
    patterns = PatternMatcher()
    with open(f'puzzle19{"-test" if testing else ""}.in', 'r') as f:
        for pattern in next(f).strip().split(', '):
            patterns.add_pattern(pattern)
        next(f)
        targets = [line.strip() for line in f]
    return patterns, targets


def part_1():
    patterns, targets = read_data()
    return sum(1 for target in targets if patterns.can_build(target))


def part_2():
    patterns, targets = read_data()
    return sum(patterns.combinations(target) for target in targets)
