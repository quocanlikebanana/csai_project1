## OLD FILE, NOT USED

# State: any position on grid (x,y; x, y is N, x > 0, y > 0) that stays in the gird and not on the polygons
# Initial state: start position.
# Action: Move to 8 adjacent tiles.
# Transition model: New position based on the direction chosen to move.
# Goal test: state position is the end position.
# Path cost: 1 cost for 4 horizontal and vertical, 1.5 cost for 4 cross.


from component.enviroment import Enviroment
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

    def action(self, method: METHODS):
        if method == METHODS.LEFT:
            return IDS_Node(self, self.state.relative(-1, 0), 1)
        elif method == METHODS.LEFT_UP:
            return IDS_Node(self, self.state.relative(-1, -1), 1.5)
        elif method == METHODS.UP:
            return IDS_Node(self, self.state.relative(0, -1), 1)
        elif method == METHODS.RIGHT_UP:
            return IDS_Node(self, self.state.relative(1, -1), 1.5)
        elif method == METHODS.RIGHT:
            return IDS_Node(self, self.state.relative(1, 0), 1)
        elif method == METHODS.RIGHT_DOWN:
            return IDS_Node(self, self.state.relative(1, 1), 1.5)
        elif method == METHODS.DOWN:
            return IDS_Node(self, self.state.relative(0, 1), 1)
        elif method == METHODS.LEFT_DOWN:
            return IDS_Node(self, self.state.relative(-1, 1), 1.5)


class IDS:
    def __init__(self, map: Enviroment) -> None:
        self.map = map
        self.goal = map.endPoint
        self.initNode = IDS_Node(None, map.startPoint, 0)
        self.curNode = self.initNode
        self.MAX_LIM = 100000
        self.done = False

    def constraint(self):
        return self.map.validatePosition(self.curNode)

    def getPointsPath(self):
        path: list[Point] = []
        tempNode = self.curNode
        while True:
            path.insert(0, self.curNode.state)
            if tempNode.parent == None:
                break
            tempNode = tempNode.parent
        return path

    def getCost(self):
        pass

    def search(self):
        if self.done == True:
            return None
        lim = 1
        curLim = 1
        frontier: list[IDS_Node] = []
        explored: list[IDS_Node] = []
        child: IDS_Node
        while lim <= self.MAX_LIM:
            curLim = lim
            explored = []
            frontier.insert(0, self.initNode)
            while curLim > 0 and len(frontier) > 0:
                self.curNode = frontier.pop(0)
                explored.append(self.curNode)
                if self.curNode.isSameState(self.goal):
                    self.done = True
                    return self.curNode
                for method in METHODS:
                    child = self.curNode.action(method)
                    if not child in explored:
                        frontier.insert(0, child)
                curLim -= 1
            lim += 1
        return None
