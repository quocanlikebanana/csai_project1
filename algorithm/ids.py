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
    def __init__(self, parent, state: Point, depth: int, cost) -> None:
        self.parent = parent
        self.state = state
        self.cost = cost
        self.depth = depth

    def isSameState(self, node):
        if self.state == node.state:
            return True
        return False

    def getChild(self, dir: DIRECTION):
        cost = 1
        if DIRECTION.isCrossDir(dir):
            cost = 1.5
        return IDS_Node(
            self, self.state.relative(dir.value.x, dir.value.y), self.depth + 1, cost
        )


class IDS(Algorithm):
    def __init__(self, env: Enviroment) -> None:
        super().__init__(env)
        self.env = env
        self.MAX_LIM = 1000
        self.curLim = 0
        self.done = False
        self.cost = None
        self.found = False
        self.frontier: list[IDS_Node] = [IDS_Node(None, self.env.startPoint, 0, 0)]
        self.env.appendClosePoint(self.env.startPoint)

    def isDone(self):
        return self.cost != None

    def resetDFS(self):
        self.env.clearFinding()
        self.curLim += 1
        self.frontier: list[IDS_Node] = [IDS_Node(None, self.env.startPoint, 0, 0)]
        self.env.appendClosePoint(self.env.startPoint)

    def searchOnce(self):
        if self.isDone() == True:
            return
        if self.curLim == self.MAX_LIM:
            raise ValueError("ids max limit, ids not found")
        if len(self.frontier) == 0:
            self.resetDFS()
        curNode = self.frontier.pop(0)
        if curNode.state == self.env.endPoint:
            self.cost = 0
            while curNode.parent != None:
                self.env.appendDonePoint(curNode.state)
                self.cost += curNode.cost
                curNode = curNode.parent
        else:
            if curNode.depth != self.curLim:
                for dir in DIRECTION:
                    if self.env.validateMove(curNode.state, dir) == True:
                        child = curNode.getChild(dir)
                        # self.frontier.append(child)  # bfs
                        self.frontier.insert(0, child)  # dfs
                        self.env.appendOpenPoint(child.state)
            self.env.appendClosePoint(curNode.state)
