from algorithm.algorithm import Algorithm
from component.enviroment import Enviroment
from component.map import DIRECTION
from component.point import Point

# Change IDS to DFS
IDS_MODE = False


class DFS_Node:
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
        return DFS_Node(
            self, self.state.relative(dir.value.x, dir.value.y), self.depth + 1, cost
        )


class DFS(Algorithm):
    def __init__(self, env: Enviroment) -> None:
        super().__init__(env)
        self.env = env
        self.MAX_LIM = 1000
        self.curLim = 0
        self.done = False
        self.cost = None
        self.found = False
        self.step = 1
        self.frontier: list[DFS_Node] = [DFS_Node(None, self.env.startPoint, 0, 0)]
        self.env.appendOpenPoint(self.env.startPoint)

    def isDone(self):
        return self.cost != None

    def resetDFS(self):
        self.env.clearFinding()
        self.curLim += self.step
        self.frontier: list[DFS_Node] = [DFS_Node(None, self.env.startPoint, 0, 0)]
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
            if IDS_MODE == False or curNode.depth != self.curLim:
                for dir in DIRECTION:
                    if self.env.validatePathMove(curNode.state, dir) == True:
                        child = curNode.getChild(dir)
                        # self.frontier.append(child)  # bfs
                        self.frontier.insert(0, child)  # dfs
                        self.env.appendOpenPoint(child.state)
            self.env.appendClosePoint(curNode.state)