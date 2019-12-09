# Specialized in finding 15 puzzle state
from Puzzle import Puzzle, Action
from typing import List
from State import State, Memory, addMemmory
import math
import numpy as np
import os
import gc

from multiprocessing import Pool, freeze_support


def getnextStack(stack: List[State]) -> List[State]:
    nextStack = []
    while len(stack) != 0:
        state = stack.pop()
        while True:
            tmp = state.getNextState()
            if not tmp:
                break
            nextStack.append(tmp)
    return nextStack


def find(size: int):
    root = State(Puzzle(size, size), Action.NONE, 0)

    Memory.clear()
    addMemmory(root)

    stack: List[State] = [root]
    depth = 0

    count = 0
    while len(stack) != 0:
        fileNo = 0
        nextStack = []
        while len(stack) != 0:
            jobs = []
            gc.collect()
            for i in range(4):
                count = 0
                tmp = []
                if 10000 < len(stack):
                    count = 10000
                else:
                    count = len(stack)
                for i in range(count):
                    tmp.append(stack.pop())
                jobs.append(tmp)
                if count != 10000:
                    break
            tmp = []
            with Pool(len(jobs)) as p:
                tmp = p.map(getnextStack, jobs)
            for i in tmp:
                for state in i:
                    if addMemmory(state):
                        nextStack.append(state)
                        count += 1

            # 저장
            while fileNo < math.floor(len(nextStack)/100000):
                save = []
                for state in nextStack[fileNo*100000:(fileNo+1)*100000]:
                    save.append(
                        [state.data.getArray(), -state.lastAction.value]
                    )
                if not os.path.exists(os.path.join(".", "data", str(size))):
                    os.mkdir(os.path.join(".", "data", str(size)))
                np.save(os.path.join(".", "data", str(size), str(
                    depth + 1) + "-" + str(fileNo)), np.array(save))
                fileNo += 1
                del(save)
        save = []
        for state in nextStack[fileNo*100000:]:
            save.append(
                [state.data.getArray(), -state.lastAction.value]
            )
        if not os.path.exists(os.path.join(".", "data", str(size))):
            os.mkdir(os.path.join(".", "data", str(size)))
        np.save(os.path.join(".", "data", str(size), str(
            depth + 1) + "-" + str(fileNo)), np.array(save))
        del(save)
        stack = nextStack
        depth += 1
        print("FINISHED" + "\t" + str(depth) + "\t" + str(len(stack)))

    return depth


if __name__ == '__main__':
    freeze_support()
    find(4)
