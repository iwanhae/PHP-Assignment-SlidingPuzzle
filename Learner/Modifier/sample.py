import numpy as np
import random
import os

outX = []
outY = []
for i in range(0, 65):
    print(i)
    def filename(x): return os.path.join(
        "data", str(x) + "-4-" + str(i) + ".npy")
    X = np.load(filename("X"), allow_pickle=True)
    Y = np.load(filename("Y"), allow_pickle=True)
    if i == 0:
        sample = range(0, len(X))
    else:
        sample = random.sample(range(0, len(X)), 10000)
    print(len(X), len(sample))
    for j in sample:
        outX.append(X[j])
        outY.append(Y[j])
np.save("X", np.array(outX))
np.save("Y", np.array(outY))
