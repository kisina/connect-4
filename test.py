import itertools

table = list(itertools.product(list(range(3)), repeat=42))

print(table)