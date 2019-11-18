import numpy as np
import math
import enum


class Action(enum.Enum):
    NONE = 0
    UP = -1
    DOWN = 1
    RIGHT = 2
    LEFT = -2


class Puzzle():
    data = np.zeros((0, 0), dtype=np.int8)
    row = 0
    col = 0
    (blankRow, blankCol) = (0, 0)

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.data = np.zeros((self.row, self.col), dtype=np.int8)
        for i in range(0, row):
            for j in range(0, col):
                self.data[i, j] = i*self.row + j

    def isPossible(self, action: Action):
        (row, col) = self.findBlank()
        if action == Action.UP:
            return row != 0
        elif action == Action.DOWN:
            return row != self.row - 1
        elif action == Action.RIGHT:
            return col != self.col - 1
        elif action == Action.LEFT:
            return col != 0

    def getArray(self) -> np.ndarray:
        return np.array(self.data)

    def Clone(self):
        p = Puzzle(self.row, self.col)
        p.data = np.array(self.data)
        return p

    def Slide(self, action: Action) -> (np.array, bool):
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

    def Up(self) -> (np.array, bool):
        (row, col) = self.findBlank()
        if row == 0:
            return np.array(self.data), False
        else:
            self.data[row, col] = self.data[row - 1, col]
            self.data[row - 1, col] = 0
            return np.array(self.data), True

    def Down(self) -> (np.array, bool):
        (row, col) = self.findBlank()
        if row == self.row - 1:
            return np.array(self.data), False
        else:
            self.data[row, col] = self.data[row + 1, col]
            self.data[row + 1, col] = 0
            return np.array(self.data), True

    def Right(self) -> (np.array, bool):
        (row, col) = self.findBlank()
        if col == self.col - 1:
            return np.array(self.data), False
        else:
            self.data[row, col] = self.data[row, col + 1]
            self.data[row, col + 1] = 0
            return np.array(self.data), True

    def Left(self) -> (np.array, bool):
        (row, col) = self.findBlank()
        if col == 0:
            return np.array(self.data), False
        else:
            self.data[row, col] = self.data[row, col - 1]
            self.data[row, col - 1] = 0
            return np.array(self.data), True
