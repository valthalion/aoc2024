from collections import defaultdict


testing = False


def read_data():
    pred_rules = defaultdict(set)
    manuals = []

    with open(f'puzzle05{"-test" if testing else ""}.in', 'r') as f:
        while (line := next(f).strip()):
            pred, succ = (int(x) for x in line.split('|'))
            pred_rules[succ].add(pred)

        manuals = [[int(x) for x in line.split(',')] for line in f]

    return pred_rules, manuals


def is_valid(manual, rules):
    contents = set(manual)
    applicable_rules = {succ: pred & contents for succ, pred in rules.items() if succ in contents and pred & contents}

    seen = set()
    for page in manual:
        seen.add(page)
        if page in applicable_rules:
            if not applicable_rules[page] <= seen:
                return False
    return True


def reorder(manual, rules):
    ordered_manual, added, pages = [], set(), set(manual)
    applicable_rules = {succ: pred & pages for succ, pred in rules.items() if succ in pages and pred & pages}
    while pages:
        page = pages.pop()
        queue = [page]
        while queue:
            page = queue[-1]
            if page in added:
                queue.pop()
                continue
            if page not in applicable_rules or applicable_rules[page] <= added:
                ordered_manual.append(page)
                added.add(page)
                queue.pop()
                continue
            queue.extend(applicable_rules[page] - added)
    return ordered_manual


def mid_page(manual):
    return manual[len(manual) // 2]


def part_1():
    pred_rules, manuals = read_data()
    return sum(mid_page(manual) for manual in manuals if is_valid(manual, pred_rules))


def part_2():
    pred_rules, manuals = read_data()
    return sum(mid_page(reorder(manual, pred_rules)) for manual in manuals if not is_valid(manual, pred_rules))
