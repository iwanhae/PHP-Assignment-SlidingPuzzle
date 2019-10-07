from agent import Agent
from pprint import pprint

agent = Agent()

Difficulty = 1
NewData = 0

while True:
    agent.initGame(count=Difficulty)
    if agent.puzzle.getScore() == 0:
        continue

    count = 0
    while not agent.isGameOver():
        count += 1
        NewData += 1
        pprint(count)
        (action, isThinking) = agent.trySolve()
        head = str(action) + ("\tMachine" if isThinking else "\t")
        pprint(head)
        pprint(agent.getArray())
        if count > 100:
            break

    if 200 < NewData:
        agent.learn()
        NewData = 0
    if agent.Clear:
        print("Hello")
        Difficulty += 1
