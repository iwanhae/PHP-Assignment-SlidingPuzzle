from collections import namedtuple
from typing import List
import random

Event = namedtuple("event", ('state', 'action', 'next_state', 'reward'))


class Memory():
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0

    def push(self, data: Event):
        if len(self.memory) < self.capacity:
            self.memory.append(data)
        else:
            self.memory[self.push_count % self.capacity] = data
        self.push_count += 1

    def getSamples(self, batch_size) -> List[Event]:
        return random.sample(self.memory, batch_size)

    def can_provide_sample(self, batch_size):
        return len(self.memory) > batch_size
