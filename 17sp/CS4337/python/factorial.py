def rec_fact(x):
    if x == 1:
        return 1
    else:
        return x * rec_fact(x-1)

def tail_fact(x, total=1):
    if x == 1:
        return total
    else:
        return tail_fact(x - 1, total * x)

def iter_fact(x):
    total = 1
    for n in range(x):
        total *= n+1
    return total

print(rec_fact(3))
print(tail_fact(3))
print(iter_fact(3))
