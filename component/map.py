from enum import Enum
from typing import Callable
from component.point import Point
from inspect import signature


class CELL_STATE(Enum):
    BLOCKED = 1
    OPEN = 2
    CLOSE = 3
    START = 4
    PICKUP = 5
    END = 6
    NONE = 7
    DONE = 8


class DIRECTION(Enum):
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    UP = Point(0, -1)
    RIGHTDOWN = Point(1, 1)
    LEFTTOP = Point(-1, -1)
    RIGHTTOP = Point(1, -1)
    LEFTDOWN = Point(-1, 1)

    @staticmethod
    def isCrossDir(dir):
        return dir.value.x != 0 and dir.value.y != 0


# This is serve for enviroment state change, not from the algorithm (like a block is moving)


class StateTrigger:
    def __init__(self, before: CELL_STATE, after: CELL_STATE, trigger) -> None:
        self._before = before
        self._after = after
        self._trigger = trigger
        pass

    def checkTriggerToCall(self, before: CELL_STATE, after: CELL_STATE, point: Point):
        if before == self._before and after == self._after:
            return self._trigger(point)
        return None


def stateTriggersFactory(openToBlock, closeToBlock, blockToNone):
    return [
        StateTrigger(CELL_STATE.OPEN, CELL_STATE.BLOCKED, openToBlock),
        StateTrigger(CELL_STATE.CLOSE, CELL_STATE.BLOCKED, closeToBlock),
        StateTrigger(CELL_STATE.BLOCKED, CELL_STATE.NONE, blockToNone),
    ]
    pass


class Cell:
    def __init__(self, point: Point) -> None:
        self._state = CELL_STATE.NONE
        self._extraInfo = None
        self._point = point
        self._manageList: list[Point] = None
        self._stateTrigger: list[StateTrigger] = []
        pass

    @property
    def point(self):
        return self._point

    @property
    def x(self):
        return self._point.x

    @property
    def y(self):
        return self._point.y

    def setTriggers(self, stateTriggers: list[StateTrigger]):
        self._stateTrigger = stateTriggers
        pass

    def getState(self):
        return self._state, self._extraInfo

    def setStateWithManageList(
        self, state: CELL_STATE, newManageList: list[Point] = None, extraInfo=None
    ):
        self._extraInfo = extraInfo
        if self._manageList != None:
            self._manageList.remove(self._point)
        if newManageList != None:
            newManageList.append(self._point)
        self._manageList = newManageList
        self._state = state

    def setStateWithTrigger(
        self, state: CELL_STATE, extraInfo=None, beforeUpdateCell=None
    ):
        self.trigger(state)
        self._extraInfo = extraInfo
        pass

    def trigger(self, state):
        for st in self._stateTrigger:
            st.checkTriggerToCall(self._state, state, self.point)
        self._state = state

    # Old
    def setState(self, state: CELL_STATE, extraInfo=None):
        self._state = state
        self._extraInfo = extraInfo  # Always reset extraInfo if not passed
        # BLOCKED with None is Border
        # Potential bug
