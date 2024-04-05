from enum import Enum
import math
from algorithm.priorityqueue import PriorityQueue
from component.enviroment import Enviroment
from component.point import Point


BLOCK_SIZE = 10
CROSS_COST = 14
STRAIGHT_COST = 10


def EuclideanHeuristic(curNode, targetNode):
    return (
        math.sqrt(
            pow((curNode.x - targetNode.x), 2) + pow((curNode.y - targetNode.y), 2)
        )
        * CROSS_COST
    )


def ManhattanHeuristic(curNode, targetNode):
    return (
        abs(curNode.x - targetNode.x) + abs(curNode.y - targetNode.y)
    ) * STRAIGHT_COST


class NodeStatus(Enum):
    BLOCKED = 1
    OPEN = 2
    CLOSE = 3
    START = 4
    END = 5
    NONE = 6
    DONE = 7


class AS_Node:
    def __init__(self, x, y, g, h, status):
        self.x = x
        self.y = y
        self.h = h
        self.g = g
        self.f = g + h
        self.status = status
        self.parent = None

    def Display(self):
        print("(", self.x, ",", self.y, ")", end="")


class AS_Map:
    def __init__(self, env: Enviroment):
        self.env = env
        self.nodes = []
        for x in range(env.ncol):
            col = []
            for y in range(env.nrow):
                col.append(AS_Node(x, y, 0, 0, NodeStatus.NONE))
            self.nodes.append(col)
        bps = env.blockPoints
        for p in bps:
            self.nodes[p.x][p.y].status = NodeStatus.BLOCKED

    def Display(self):
        for col in self.nodes:
            for node in col:
                node.Display()
            print("")

    def GetNeighbours(self, node):
        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ]
        neighbours = []
        curX = node.x
        curY = node.y
        for i, (dx, dy) in enumerate(directions):
            nx, ny = curX + dx, curY + dy
            if 0 <= nx < len(self.nodes) and 0 <= ny < len(self.nodes[0]):
                neighbour = self.nodes[nx][ny]
                if (
                    neighbour.status != NodeStatus.BLOCKED
                    and neighbour.status != NodeStatus.OPEN
                    and neighbour.status != NodeStatus.CLOSE
                    and neighbour.status != NodeStatus.START
                ):
                    if i in [0, 1, 2, 3]:
                        neighbour.g = node.g + STRAIGHT_COST
                    else:
                        neighbour.g = node.g + CROSS_COST
                    neighbours.append(neighbour)
        return neighbours


class AStar:
    def __init__(self, map: AS_Map, heuristicFunction) -> None:
        self.startNode = map.nodes[map.env.startPoint.x][map.env.startPoint.y]
        self.targetNode = map.nodes[map.env.endPoint.x][map.env.endPoint.y]
        self.startNode.status = NodeStatus.START
        self.targetNode.status = NodeStatus.END
        self.open = PriorityQueue()
        self.open.insert(self.startNode)
        self.close = PriorityQueue()
        self.heuristicFunction = heuristicFunction
        self.map = map
        self.searching = True

    def searchOnce(self):
        if self.searching == False:
            return False
        else:
            currentNode = self.open.delete()
            self.close.insert(currentNode)
            if currentNode != self.startNode:
                currentNode.status = NodeStatus.CLOSE
                self.map.env.closedPoints.append(Point(currentNode.x, currentNode.y))
            if currentNode == self.targetNode:
                self.searching = False
                # print(currentNode.f)
                currentNode.status = NodeStatus.END
                while currentNode.parent != self.startNode:
                    currentNode.parent.status = NodeStatus.DONE
                    self.map.env.donePoints.append(
                        Point(currentNode.parent.x, currentNode.parent.y)
                    )
                    currentNode = currentNode.parent
            else:
                Neighbours = []
                Neighbours = self.map.GetNeighbours(currentNode)
                for node in Neighbours:
                    node.parent = currentNode
                    node.h = self.heuristicFunction(node, self.targetNode)
                    node.f = node.g + node.h
                    node.status = NodeStatus.OPEN
                    self.map.env.openedPoints.append(Point(node.x, node.y))
                    self.open.insert(node)
            return True
