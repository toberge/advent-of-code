def mkrule(rule: str):
    num, rule = rule.split(": ")
    num = int(num)
    if len(rule) > 2 and rule[0] == rule[2] == '"':
        return (num, rule[1])
    if rule.find("|") > 0:
        idx = rule.find("|")
        return (
            num,
            [
                list(map(int, rule[:idx].split())),
                list(map(int, rule[idx + 1 :].split())),
            ],
        )
    return (num, list(map(int, rule.split())))


def parse_rules(lines: [str]) -> []:
    rules = sorted(map(mkrule, lines), key=lambda t: t[0])
    # asserts to make sure input has all nums from 0 to whatever
    assert all(rules[i][0] < rules[i + 1][0] for i in range(len(rules) - 1))
    maxdiff = max(rules[i + 1][0] - rules[i][0] for i in range(len(rules) - 1))
    if maxdiff == 1:
        return [t[1] for t in rules]
    # Handle the second assertion's failure in part 2's example
    lst = [None] * max(t[0] + 1 for t in rules)
    for i, rule in rules:
        lst[i] = rule
    return lst
