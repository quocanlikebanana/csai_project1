import math
from algorithm.algorithm import Algorithm
from component.environment import Environment
from component.map import CELL_STATE, DIRECTION, Cell, stateTriggersFactory
from component.point import Point


class DS_Node:
    def __init__(self, state: Point, g: float, rhs: float, algoHFunc) -> None:
        self.state = state
        self.g = g
        self.h = algoHFunc(self)
        self.rhs = rhs
        self.blocked = False
        self.successorGradient: DS_Node = None
        self.charSymbol = "·"
        pass

    # Key != f; k = [k(1), k(2)]
    def getKeys(self):
        return [min(self.g, self.rhs) + self.h, min(self.g, self.rhs)]

    def updateKeys(self, g, rhs):
        self.g = g
        self.rhs = rhs
        pass

    def isConsistent(self):
        return self.g == self.rhs


# 1: gt, 0: eq, -1 lt
def keyCompare(key1, key2):
    if key1[0] > key2[0]:
        return 1
    if key1[0] < key2[0]:
        return -1
    if key1[1] > key2[1]:
        return 1
    if key1[1] < key2[1]:
        return -1
    return 0


# NO duplicate keys
class DS_Frontier:
    def __init__(self) -> None:
        self._list: list[DS_Node] = []
        pass

    def isEmpty(self):
        return len(self._list) == 0

    def topKey(self):
        if len(self._list) == 0:
            return [math.inf, math.inf]
        return self._list[0].getKeys()

    def update(self, node: DS_Node):
        if node in self._list:
            self._list.remove(node)
        j = 0
        l = len(self._list)
        nodeKeys = node.getKeys()
        while j < l:
            keys = self._list[j].getKeys()
            if keys[0] > nodeKeys[0] or (
                keys[0] == nodeKeys[0] and keys[1] >= nodeKeys[1]
            ):
                break
            j += 1
        self._list.insert(j, node)
        pass

    def pop(self) -> DS_Node:
        return self._list.pop(0)


DIS_COST = 1


def EuclideanHeuristic(curNode: DS_Node, target: Point):
    return (
        math.sqrt(
            pow((curNode.state.x - target.x), 2) + pow((curNode.state.y - target.y), 2)
        )
        * DIS_COST
    )


def ManhattanHeuristic(curNode: DS_Node, target: Point):
    return (
        abs(curNode.state.x - target.x) + abs(curNode.state.y - target.y)
    ) * DIS_COST


# Remember: predecessor is from start to goal (otherwise successor)
# Successor are the same as Predecessor here


class DStar(Algorithm):
    def __init__(self, env: Environment, hFunc=EuclideanHeuristic) -> None:
        super().__init__(env)
        self.env = env
        self.done = False
        self.doneCompute = False
        self.hFunc = hFunc
        self.agentNode: DS_Node = None
        self.map = [
            [
                DS_Node(Point(x, y), math.inf, math.inf, self._getHeuristic)
                for y in range(self.env.nrow)
            ]
            for x in range(self.env.ncol)
        ]
        self.env.onPolygonMoveTrigger = self.onPolygonMove
        self.affectedPoints: list[Point] = []
        self.init()
        self.computePath()
        self.findPath()

    def getAdjacent(self, node: DS_Node):
        result: list[tuple[DS_Node, float, DIRECTION]] = []
        for dir in DIRECTION:
            test = node.state.relative(dir.value.x, dir.value.y)
            if self.env.checkInBorder(test):
                cost = math.inf
                checkDir = self.env.checkNotOnPolygon(test)
                checkSelf = self.env.checkNotOnPolygon(node.state)
                if checkDir and checkSelf:
                    cost = 1 if DIRECTION.isCrossDir(dir) == False else 1.4
                result.append(
                    [self.map[test.x][test.y], cost, DIRECTION.getSymbol(dir)]
                )
        return result

    def init(self):
        self.goalNode = self.map[self.env.endPoint.x][self.env.endPoint.y]
        self.goalNode.rhs = 0
        self.frontier = DS_Frontier()
        self.frontier.update(self.goalNode)
        self.agentNode = self.map[self.env.startPoint.x][self.env.startPoint.y]
        self.env.agentPoint = self.agentNode.state

    def _getHeuristic(self, curNode: DS_Node):
        return self.hFunc(curNode, self.env.endPoint)

    def computePath(self):
        while True:
            # if self.frontier.isEmpty():
            #     printMap(self.map)
            #     print("============")
            #     printEnvMap(self.env.map)
            if not (
                self.agentNode.isConsistent() == False
                or keyCompare(self.frontier.topKey(), self.agentNode.getKeys()) == -1
            ):
                # printMap(self.map)
                # print("============")
                # printEnvMap(self.env.map)
                break
            node = self.frontier.pop()
            if node.g > node.rhs:
                node.g = node.rhs
            elif node.g < node.rhs:
                node.g = math.inf
                self.updateNode(node)  # Will update is self when underscore
            pre = self.getAdjacent(node)
            for p in pre:
                self.updateNode(p[0])
            pass
        self.doneCompute = True
        # print("=" * 50)
        # printMapDir(self.map)
        # print("*" * 10)
        # printEnvMap(self.env.map)
        # print("=" * 50)
        pass

    def updateNode(self, node: DS_Node):
        if node.state != self.goalNode.state:
            suc = self.getAdjacent(node)
            node.successorGradient = None
            node.charSymbol = "·"
            # Note: min here doesnt include itself
            if len(suc) > 0:
                minrhs = suc[0][0].g + suc[0][1]
                sucGrad = suc[0][0]
                charSym = suc[0][2]
                for s in suc:
                    if s[0].g + s[1] < minrhs:
                        minrhs = s[0].g + s[1]
                        sucGrad = s[0]
                        charSym = s[2]
                node.rhs = minrhs
                if minrhs != math.inf:
                    node.successorGradient = sucGrad
                    node.charSymbol = charSym
            if node.isConsistent() == False:
                self.frontier.update(node)
        pass

    def onPolygonMove(self, points: list[Point]):
        # vẫn còn hơi conflict chỗ này do đang update point thì đa giác lại di chuyển (xài doneCompute như semaphore)
        if self.doneCompute == True:
            self.affectedPoints = points
        pass

    def searchOnce(self):
        if self.done == True:
            return
        if len(self.affectedPoints) > 0:
            self.env.allowMove = False
            self.env.closedPoints.clear()
            for p in self.affectedPoints:
                self.updateNode(self.map[p.x][p.y])
            self.done = False
            self.doneCompute = False
            self.computePath()
            self.findPath()
            self.affectedPoints.clear()
            self.env.allowMove = True
        if self.agentNode.state != self.goalNode.state:
            if self.agentNode.g == math.inf:
                raise ValueError("dstar not found")
            # If path still found
            self.env.donePoints.append(self.agentNode.state)
            self.agentNode = self.agentNode.successorGradient
            self.env.agentPoint = self.agentNode.state
        else:
            self.done = True
        pass

    def findPath(self):
        traversalStart = self.agentNode
        while traversalStart.successorGradient != None:
            self.env.closedPoints.append(traversalStart.state)
            traversalStart = traversalStart.successorGradient


def printMap(map: list[list[DS_Node]]):
    ncol = len(map)
    nrow = len(map[0])
    for y in range(nrow):
        for x in range(ncol):
            if map[x][y].g == math.inf:
                print("X", end="  ")
            else:
                print("O", end="  ")
        print()


def printEnvMap(map: list[list[Cell]]):
    ncol = len(map)
    nrow = len(map[0])
    for y in range(nrow):
        for x in range(ncol):
            if map[x][y].getState()[0] == CELL_STATE.BLOCKED:
                print("X", end="  ")
            else:
                print("O", end="  ")
        print()


def printMapDir(map: list[list[DS_Node]]):
    ncol = len(map)
    nrow = len(map[0])
    for y in range(nrow):
        for x in range(ncol):
            print(map[x][y].charSymbol, end="  ")
        print()
