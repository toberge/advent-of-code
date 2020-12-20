from bags import parse_bags

lookup, rules = parse_bags(open("example.dat", "r").readlines())
f = lambda target: [(count, f(bag)) for bag, count in rules[target]]
print(f("shiny gold"))
