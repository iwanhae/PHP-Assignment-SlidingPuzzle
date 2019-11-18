from Puzzle import Puzzle, Action
from typing import List
from State import State, Memory, addMemmory
import math
import numpy as np
import os

from multiprocessing import Pool

# finding possible state of 1 3 8 15 24 35 48 63 80 99 puzzle until FINDMAX
FINDMAX = 200000


def find(size: int):
    root = State(Puzzle(size, size), Action.NONE, 0)

    Memory.clear()
    addMemmory(root)

    stack: List[State] = [root]
    depth = 0

    count = 0
    while len(stack) != 0:
        nextStack: List[State] = []
        while len(stack) != 0:
            state = stack.pop()
            while True:
                tmp = state.getNextState()
                if not tmp:
                    break
                nextStack.append(tmp)
                count += 1
            if count > FINDMAX:
                break
        stack = nextStack
        depth += 1
        print(str(size) + "\t" + str(depth) + "\t" + str(len(stack)))

        save = []
        for state in stack:
            save.append([state.data.getArray(), -state.lastAction.value])
        if not os.path.exists(os.path.join(".", "data", str(size))):
            os.mkdir(os.path.join(".", "data", str(size)))
        np.save(os.path.join(".", "data", str(size), str(depth)), np.array(save))
        del(save)
        if count > FINDMAX:
            break
    return depth


with Pool(8) as p:
    print(p.map(find, [3, 4, 5, 6, 7, 8, 9, 10]))
