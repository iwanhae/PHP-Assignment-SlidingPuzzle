from actionEnum import Action
from puzzleState import puzzleState
from random import randint, random
from dqn import DQN, Event
import numpy as np


class Agent:
    EPS = 1
    EPS_END = 0.01
    EPS_DECAY = 0.0001
    LAST_ACTION = Action.NONE
    GameOver = False
    Clear = False

    def __init__(self):
        self.puzzle = puzzleState()
        self.dqn = DQN()

    def initGame(self, count=10):
        self.GameOver = False
        self.Clear = False
        self.puzzle = puzzleState()
        for i in range(count):
            self.puzzle.Slide(Action(randint(0, 3)))
        return self.puzzle.getArray()

    def isGameOver(self) -> bool:
        if self.GameOver:
            return True
        elif self.puzzle.getScore() == 0:
            self.Clear = True
            return True
        else:
            return False

    def trySolve(self):
        action = Action.NONE
        isThinking = False

        if random() < self.EPS:   # 초반엔 임의로 행동을 주로함.
            action = self.puzzle.getBestAction()
        else:
            isThinking = True
            (_, _, answer) = self.dqn.guess(self.puzzle.getArray())

            answer[Action.getReverseAction(self.LAST_ACTION).value] = -10
            action = Action(np.argmax(answer))
            if not self.puzzle.isPossible(action):
                answer[action.value] = -10
                action = Action(np.argmax(answer))
            if not self.puzzle.isPossible(action):
                answer[action.value] = -10
                action = Action(np.argmax(answer))

        if action == Action.NONE:
            self.GameOver = True
            return (action, isThinking)

        self.LAST_ACTION = action
        if self.EPS_END < self.EPS:
            self.EPS -= self.EPS_DECAY

        state = np.array(self.puzzle.getScoreMatrix())

        prevScore = self.puzzle.getScore()

        success = self.puzzle.Slide(action)

        reward = self.puzzle.getScore() - prevScore
        if not success:
            self.GameOver = True
            reward = -1

        next_state = np.array(self.puzzle.getScoreMatrix())

        if not reward == 0:
            self.dqn.remember(Event(state, action, next_state, reward))
        return (action, isThinking)

    def learn(self):
        self.dqn.train()

    def getArray(self):
        return self.puzzle.getArray()
