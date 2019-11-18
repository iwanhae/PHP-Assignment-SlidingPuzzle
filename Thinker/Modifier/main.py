from puzzle2Map import puzzle2Map
import matplotlib.pyplot as plt
import numpy as np
import math

from multiprocessing import Pool

import os

Action = {
    -2: 0,
    -1: 1,
    1: 2,
    2: 3
}
onehot = np.eye(4)

cmap = plt.cm.jet
norm = plt.Normalize(vmin=0, vmax=2)


def convert(num: int):
    X = []
    Y = []
    for file in os.listdir(os.path.join("input", str(num))):
        print(str(num) + "\t" + file)
        data = np.load(os.path.join(
            "input", str(num), file), allow_pickle=True)
        for d in data:
            action = onehot[Action[d[1]]]
            d = d[0]
            d = puzzle2Map(d)

            X.append(d)
            Y.append(action)
    np.save(os.path.join("data", "X-" + str(num)), X)
    np.save(os.path.join("data", "Y-" + str(num)), Y)
    print(str(num) + "\tfinished\t" + str(len(X)))

    count = 0
    if not os.path.exists(os.path.join(".", "data", str(num))):
        os.mkdir(os.path.join(".", "data", str(num)))
    for x in X:
        plt.imsave(os.path.join("data", str(num), str(count)+".bmp"), cmap(norm(x)))
        count += 1
        if count == 1024:
            break
    return len(X)

convert(8)
#with Pool(10) as p:
#    print(p.map(convert, [1,2,3,4,5,6,7,8,9,10]))
