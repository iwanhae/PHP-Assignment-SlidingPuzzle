import numpy as np
import math
from actionEnum import Action


def calcScore(arr: np.array) -> np.array:
    score = np.empty(arr.shape)
    (row, col) = arr.shape
    for i in range(0, row):
        for j in range(0, col):
            val = arr[i, j]
            if val == 0:
                score[i, j] = -1
                continue
            (dRow, dCol) = (math.floor(val/row), val % row)
            score[i, j] = (abs(dRow - i) + abs(dCol - j)) / (row + col)
    return score


class puzzleState():
    data = np.zeros((3, 3), dtype=np.int8)
    row = 3
    col = 3
    (blankRow, blankCol) = (0, 0)

    def __init__(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.data[i, j] = i*self.row + j

    def isPossible(self, action):
        (row, col) = self.findBlank()
        if action == Action.UP:
            return row != 0
        elif action == Action.DOWN:
            return row != self.row - 1
        elif action == Action.RIGHT:
            return col != self.col - 1
        elif action == Action.LEFT:
            return col != 0

    def getBestAction(self):
        bestAction = Action.NONE
        score = self.getScore()
        max_score = 0

        for i in range(4):
            action = Action(i)
            if self.Slide(action):
                gap = self.getScore() - score
                if max_score < gap:
                    max_score = gap
                    bestAction = action
                self.Slide(Action.getReverseAction(action))

        return bestAction

    def getScore(self) -> np.float:
        return -(np.sum(self.getScoreMatrix()) + 1)  # 0이 가장 높은 값

    def getScoreMatrix(self) -> np.array:
        return calcScore(self.data)

    def getArray(self) -> np.array:
        return self.data

    def Slide(self, action: Action) -> bool:
        if action == Action.UP:
            return self.Up()
        elif action == Action.DOWN:
            return self.Down()
        elif action == Action.RIGHT:
            return self.Right()
        elif action == Action.LEFT:
            return self.Left()

    def findBlank(self) -> (np.int64, np.int64):
        if self.data[self.blankRow, self.blankCol] == 0:
            return (self.blankRow, self.blankCol)
        else:
            (row, col) = np.where(self.data == 0)
            (self.blankRow, self.blankCol) = (row[0], col[0])
            return (self.blankRow, self.blankCol)

    def Up(self) -> bool:
        (row, col) = self.findBlank()
        if row == 0:
            return False
        else:
            self.data[row, col] = self.data[row - 1, col]
            self.data[row - 1, col] = 0
            return True

    def Down(self) -> bool:
        (row, col) = self.findBlank()
        if row == self.row - 1:
            return False
        else:
            self.data[row, col] = self.data[row + 1, col]
            self.data[row + 1, col] = 0
            return True

    def Right(self) -> bool:
        (row, col) = self.findBlank()
        if col == self.col - 1:
            return False
        else:
            self.data[row, col] = self.data[row, col + 1]
            self.data[row, col + 1] = 0
            return True

    def Left(self) -> bool:
        (row, col) = self.findBlank()
        if col == 0:
            return False
        else:
            self.data[row, col] = self.data[row, col - 1]
            self.data[row, col - 1] = 0
            return True
