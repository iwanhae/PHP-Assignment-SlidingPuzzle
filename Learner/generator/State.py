from __future__ import annotations

from Puzzle import Puzzle, Action
from typing import List, Dict
import math
import numpy as np

Memory: Dict[int, State] = {}


def addMemmory(state: State) -> bool:
    key = hash(state.id)
    if key in Memory:
        return False
    else:
        Memory[key] = 1  # state
        return True


def hue(puzzle: Puzzle) -> float:
    return 0
    data = puzzle.getArray()
    (col, row) = data.shape
    for i in range(row):
        for j in range(col):
            pos = data[i][j]
            r = pos / col
            c = pos % col
            data[i][j] = abs(i - r) + abs(j - c)
    return data.sum()


class tmpState():
    score: int
    action: Action


class State():
    data: Puzzle
    id: int
    depth: int
    score: float
    offset: int = 0
    lastAction: Action
    nextState: List[tmpState] = []
    parent: int

    def __init__(self, puzzle: Puzzle, lastAction: Action,  depth: int, parent: int = 0):
        self.data = puzzle.Clone()
        self.id = str(puzzle.getArray())
        self.depth = depth
        self.score = hue(puzzle) + depth
        self.nextState = []
        self.lastAction = lastAction
        self.parent = parent

        for i in range(-2, 3):  # -2 - 1 1 2
            if i == 0:
                continue
            action = Action(i)
            if self.data.isPossible(action):
                (data, _) = self.data.Slide(action)
                state = tmpState()
                state.score = hue(self.data) + depth + 1
                state.action = action
                id = str(self.data.getArray())
                self.nextState.append(state)
                self.data.Slide(Action(-i))
        self.nextState = sorted(self.nextState, key=lambda x: x.score)

    def setOffset(self, offset: int):
        self.offset = offset

    def getScore(self) -> int:
        return self.depth + self.score

    def getNextState(self) -> State:
        while len(self.nextState) > self.offset:
            tmp = self.nextState[self.offset]
            self.offset += 1
            puzzle = self.data.Clone()
            puzzle.Slide(tmp.action)
            tmp = State(puzzle, tmp.action, self.depth + 1, self.id)
            if addMemmory(tmp):
                return tmp
            else:
                continue
        return False
