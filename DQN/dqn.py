import tensorflow as tf
import numpy as np
import random

from actionEnum import Action
from memory import Memory, Event
from DQNModel import DQNModel


class DQN():
    MAX_MEMORY = 1000
    BATCH_SIZE = 32
    GAMMA = 0.5    # 미래에 대한 가중치

    def __init__(self):
        super(DQN, self).__init__()
        self.Model = DQNModel()
        self.Memory = Memory(self.MAX_MEMORY)

    def train(self):
        if self.Memory.push_count < 200:
            return
        samples = self.Memory.getSamples(200)
        states = []
        actions = []
        targets = []
        for event in samples:
            states.append(event.state)

            (action, reward, _) = self.guess(event.next_state)

            actions.append(action)
            target = (1-self.GAMMA)*event.reward + self.GAMMA * reward
            targets.append(target)

        states = np.array(states)
        actions = np.array(actions)
        targets = np.array(targets)

        self.Model.train(states, actions, targets)

    def guess(self, x) -> (int, float, np.array):
        x = np.array([x])
        answer = np.array(self.Model.call(x)[0])
        action = np.argmax(answer)
        reward = answer[action]
        return (action, reward, answer)

    def remember(self, event: Event):
        self.Memory.push(event)
