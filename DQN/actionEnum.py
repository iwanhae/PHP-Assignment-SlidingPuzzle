import enum


class Action(enum.Enum):
    NONE = 4
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3

    def getReverseAction(action):
        if action == Action.UP:
            return Action.DOWN
        elif action == Action.DOWN:
            return Action.UP
        elif action == Action.RIGHT:
            return Action.LEFT
        elif action == Action.LEFT:
            return Action.RIGHT
        else:
            return action
