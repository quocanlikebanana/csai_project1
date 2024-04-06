from enum import Enum
from component.point import Point


class CELL_STATE(Enum):
    BLOCKED = 1
    OPEN = 2
    CLOSE = 3
    START = 4
    PICKUP = 5
    END = 6
    NONE = 7
    DONE = 8


class Cell:
    def __init__(self, point: Point, state: CELL_STATE, extraInfo=None) -> None:
        self.x = point.x
        self.y = point.y
        self._state = state
        self._extraInfo = extraInfo
        pass

    def setState(self, state: CELL_STATE, extraInfo=None):
        self._state = state
        self._extraInfo = extraInfo  # Always reset extraInfo if not passed
        # BLOCKED with None is Border

    def getState(self):
        return self._state, self._extraInfo
