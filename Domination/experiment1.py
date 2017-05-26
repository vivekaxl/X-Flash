from __future__ import division
from non_dominated_sort import non_dominated_sort
from domination import cdom_non_dominated_sort
from utility import read_file, lessismore

data_folder = "../Data/"
# files = ['llvm_input.csv', 'noc_CM_log.csv', 'rs-6d-c3.csv', 'sort_256.csv', 'wc+rs-3d-c4.csv', 'wc+sol-3d-c4.csv', 'wc+wc-3d-c4.csv', 'wc-3d-c4.csv', 'wc-5d-c5.csv', 'wc-6d-c1.csv', 'wc-c1-3d-c1.csv', 'wc-c3-3d-c1.csv']
files = [ 'sort_256.csv', 'wc+rs-3d-c4.csv', 'wc+sol-3d-c4.csv', 'wc+wc-3d-c4.csv', 'wc-3d-c4.csv', 'wc-5d-c5.csv', 'wc-6d-c1.csv', 'wc-c1-3d-c1.csv', 'wc-c3-3d-c1.csv']

for file in files:

    print "File: ", file
    # Actual PF
    data = read_file(data_folder + file)
    dependents = [d.objectives for d in data]
    pf_indexes = non_dominated_sort(dependents, lessismore[file])
    pf = [dependents[i] for i in pf_indexes]
    pf = sorted(pf, key=lambda x: x[0])
    print "Actual PF: ", len(pf)


    # Indicator-based PF
    cdom_pf = cdom_non_dominated_sort(dependents, lessismore[file])
    cdom_pf = sorted(cdom_pf, key=lambda x: x[0])
    print "Indicator-based: ", len(cdom_pf)
    print

    import matplotlib.pyplot as plt

    plt.title(file[:-4])
    plt.scatter([d[0] for d in dependents], [d[1] for d in dependents], color='r', label='raw')
    plt.plot([p[0] for p in pf], [p[1] for p in pf], color='green', marker='x', label='actual-pf')
    plt.scatter([p[0] for p in cdom_pf], [p[1] for p in cdom_pf], color='blue', marker='o', s=55, label='cdom')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03),
          ncol=3, fancybox=True, shadow=True)
    plt.savefig('./Figures/' + file[:-4] + ".png")

    plt.cla()