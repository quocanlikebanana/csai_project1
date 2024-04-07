## OLD FILE, NOT USED

# State: any position on grid (x,y; x, y is N, x > 0, y > 0) that stays in the gird and not on the polygons
# Initial state: start position.
# Action: Move to 8 adjacent tiles.
# Transition model: New position based on the direction chosen to move.
# Goal test: state position is the end position.
# Path cost: 1 cost for 4 horizontal and vertical, 1.5 cost for 4 cross.


from algorithm.algorithm import Algorithm
from component.enviroment import Enviroment
from component.map import DIRECTION
from component.point import Point
from enum import Enum


class METHODS(Enum):
    LEFT = 1
    LEFT_UP = 2
    UP = 3
    RIGHT_UP = 4
    RIGHT = 5
    RIGHT_DOWN = 6
    DOWN = 7
    LEFT_DOWN = 8


class IDS_Node:
    def __init__(self, parent, state: Point, cost) -> None:
        self.parent = parent
        self.state = state
        self.cost = cost

    def isSameState(self, node):
        if self.state == node.state:
            return True
        return False

    def getChild(self, dir: DIRECTION):
        cost = 1
        if DIRECTION.isCrossDir(dir):
            cost = 1.5
        return IDS_Node(self, self.state.relative(dir.value.x, dir.value.y), cost)


class IDS(Algorithm):
    def __init__(self, env: Enviroment) -> None:
        super().__init__(env)
        self.env = env
        self.MAX_LIM = 100000
        self.done = False
        self.cost = None
        self.found = False
        self.frontier: list[IDS_Node] = [IDS_Node(None, env.startPoint, 0)]

    def isDone(self):
        return self.cost != None

    def searchOnce(self):
        if self.isDone() == True:
            return
        if len(self.frontier) == 0:
            raise ValueError("ids not found")
        curNode = self.frontier.pop(0)
        self.env.appendClosePoint(curNode.state)
        if curNode.state == self.env.endPoint:
            self.cost = 0
            while curNode.parent != None:
                self.env.appendDonePoint(curNode.state)
                self.cost += curNode.cost
                curNode = curNode.parent
        else:
            for dir in DIRECTION:
                if self.env.validateMove(curNode.state, dir) == True:
                    child = curNode.getChild(dir)
                    self.frontier.insert(-1, child)
                    self.env.appendOpenPoint(child.state)
