import math
from utility import read_file


def normalize(x, min, max):
    tmp = float((x - min)) / (max - min + 0.000001)
    if tmp > 1: return 1
    elif tmp < 0: return 0
    else: return tmp


def loss(x1, x2, mins=None, maxs=None):
    # normalize if mins and maxs are given
    if mins and maxs:
        x1 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x1)]
        x2 = [normalize(x, mins[i], maxs[i]) for i, x in enumerate(x2)]

    o = min(len(x1), len(x2))  # len of x1 and x2 should be equal
    temp = sum([-1*math.exp((x2i - x1i) / o) for x1i, x2i in zip(x1, x2)]) / o
    # print x1, x2, temp
    return temp


def cdom_non_dominated_sort(objectives, lessismore):
    dependents = []
    for rd in objectives:
        temp = []
        for i in xrange(len(lessismore)):
            # if lessismore[i] is true - Minimization else Maximization
            if lessismore[i] is False:
                temp.append(-1 * rd[i])
            else:
                temp.append(rd[i])
        dependents.append(temp)

    maxs = []
    mins = []
    for i in xrange(len(objectives[0])):
         maxs.append(max([o[i] for o in dependents]))
         mins.append(min([o[i] for o in dependents]))

    non_dominated_solutions = []
    for i, oi in enumerate(dependents):
        sum_store = 0
        for j, oj in enumerate(dependents):
            if i!=j:
                # print oi, oj, loss(oi, oj, mins, maxs), loss(oj, oi, mins, maxs)
                if loss(oi, oj, mins, maxs) > loss(oj, oi, mins, maxs):
                    sum_store += 1
        if sum_store == 0:
            non_dominated_solutions.append(objectives[i])
    return non_dominated_solutions

if __name__ == "__main__":
    data = read_file("../Data/llvm_input.csv")
    dependents = [d.objectives for d in data]
    pf = cdom_non_dominated_sort(dependents, [False, False])
    pf = sorted(pf, key=lambda x:x[0])

    print len(pf)

    import matplotlib.pyplot as plt
    plt.scatter([d[0] for d in dependents], [d[1] for d in dependents], color='r')
    plt.plot([p[0] for p in pf], [p[1] for p in pf], color='green', marker='o')
    plt.show()