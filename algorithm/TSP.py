from enum import Enum
import math
import copy
import time
from algorithm.priorityqueue import PriorityQueue
from component.environment import Environment
from component.point import Point


BLOCK_SIZE = 10
CROSS_COST = 2**0.5
STRAIGHT_COST = 1
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


def EuclideanHeuristic(curNode, targetNode):
    cost = CROSS_COST
    if curNode.x - targetNode.x == 0 or curNode.y - targetNode.y == 0:
        cost = STRAIGHT_COST
    return (
        math.sqrt(
            pow((curNode.x - targetNode.x), 2) + pow((curNode.y - targetNode.y), 2)
        )
        * cost
    )


class NodeStatus(Enum):
    BLOCKED = 1
    OPEN = 2
    CLOSE = 3
    START = 4
    END = 5
    NONE = 6
    DONE = 7
    PICKUP = 8


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
    def __init__(self, env: Environment):
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
        neighbours = []
        curX = node.x
        curY = node.y
        for i, (dx, dy) in enumerate(directions):
            nx, ny = curX + dx, curY + dy
            if 0 <= nx < len(self.nodes) and 0 <= ny < len(self.nodes[0]):
                neighbour = copy.deepcopy(self.nodes[nx][ny])
                if (
                    neighbour.status != NodeStatus.BLOCKED
                    # and neighbour.status != NodeStatus.OPEN
                    and neighbour.status != NodeStatus.CLOSE
                    and neighbour.status != NodeStatus.START
                ):
                    # Kiem tra canh cheo cua PX
                    if i in [0, 1, 2, 3]:
                        neighbour.g = node.g + STRAIGHT_COST
                        neighbours.append(neighbour)
                    else:
                        if not (
                            self.nodes[curX + dx][curY].status == NodeStatus.BLOCKED
                            and self.nodes[curX][curY + dy].status == NodeStatus.BLOCKED
                        ):
                            neighbour.g = node.g + CROSS_COST
                            neighbours.append(neighbour)

        return neighbours


class Edge:
    def __init__(self, nodes, cost, vertex):
        self.nodes = nodes
        self.vertex = vertex
        self.cost = cost

    def MakeDone(self, map: AS_Map):
        for node in self.nodes:
            map.env.appendDonePoint(Point(node.x, node.y))
            # map.env.appendDonePoint(Point(node.x,node.y))

    def MakeNone(self, map: AS_Map):
        for node in self.nodes:
            for i in map.env.donePoints:
                if i == Point(node.x, node.y):
                    map.env.donePoints.remove(i)

    def HasVertex(self, vertex):
        for i in vertex:
            if i in self.vertex:
                continue
            else:
                return False
        return True


def FindEdge(nodes, map):
    Edge = []
    for node in nodes:
        return


def Astar(map: AS_Map, startPoint, endPoint, heuristicFunction):
    startNode = map.nodes[startPoint.x][startPoint.y]
    targetNode = map.nodes[endPoint.x][endPoint.y]
    startNode.status = NodeStatus.START
    targetNode.status = NodeStatus.END
    open = PriorityQueue()
    open.insert(startNode)
    close = PriorityQueue()
    searching = True
    nodeArr = []
    cost = 0
    while searching:
        if open.isEmpty():
            raise ValueError("astar not found")
        currentNode = open.delete()

        close.insert(currentNode)
        if currentNode != startNode:
            currentNode.status = NodeStatus.CLOSE
        if currentNode == targetNode:
            cost = currentNode.f
            searching = False
            currentNode.status = NodeStatus.END
            while currentNode.parent != startNode:
                currentNode.parent.status = NodeStatus.DONE
                nodeArr.append(currentNode.parent)
                currentNode = currentNode.parent
        else:
            Neighbours = []
            Neighbours = map.GetNeighbours(currentNode)

            for node in Neighbours:
                node.h = heuristicFunction(node, targetNode)
                node.f = node.g + node.h
                realNode = map.nodes[node.x][node.y]
                if node.f < realNode.f or realNode.status != NodeStatus.OPEN:
                    realNode.g = node.g
                    realNode.h = node.h
                    realNode.f = node.f
                    realNode.parent = currentNode
                    if realNode.status != NodeStatus.OPEN:
                        realNode.status = NodeStatus.OPEN
                        # self.map.env.appendOpenPoint(Point(node.x, node.y))
                        open.insert(realNode)
    return nodeArr, cost


class TSP:
    def __init__(self, env, heuristicFunction=EuclideanHeuristic) -> None:
        self.map = AS_Map(env)
        self.listV = []
        self.listV.append(self.map.nodes[env.startPoint.x][env.startPoint.y])
        for point in self.map.env.pickupPoints:
            self.listV.append(self.map.nodes[point.x][point.y])
        self.listV.append(
            self.map.nodes[self.map.env.endPoint.x][self.map.env.endPoint.y]
        )
        self.heuristicFunction = heuristicFunction
        self.searching = True
        self.Edges = []
        self.Dist = [
            [0.0 for _ in range(len(self.listV))] for _ in range(len(self.listV))
        ]
        for i in range(len(self.listV) - 1):
            for j in range(i + 1, len(self.listV)):
                mapCopy = copy.deepcopy(self.map)
                nodes, cost = Astar(
                    mapCopy, self.listV[i], self.listV[j], self.heuristicFunction
                )
                self.Edges.append(Edge(nodes, cost, [self.listV[i], self.listV[j]]))
                self.Dist[i][j] = cost
                self.Dist[j][i] = cost
        self.c = [i for i in range(len(self.listV))]
        self.endIndex = len(self.listV)
        self.minCost, self.path = self.tsp(self.c, 0)
        self.currentVIndex = 0

    def searchOnce(self):
        if self.searching:
            time.sleep(0.3)
            if self.currentVIndex >= len(self.listV) - 2:
                print("Path:", self.path)
                print("Cost: ", self.minCost)
                self.searching = False
            for edge in self.Edges:
                if edge.HasVertex(
                    [
                        self.listV[self.path[self.currentVIndex]],
                        self.listV[self.path[self.currentVIndex + 1]],
                    ]
                ):
                    edge.MakeDone(self.map)
            self.currentVIndex += 1
        else:

            return True

    def tsp(self, c, v):
        if len(c) == 2 and c[0] != c[1]:
            return self.Dist[c[0]][c[1]], [c[0], c[1]]
        subArr = copy.deepcopy(c)
        subArr.remove(v)
        minCost = float("inf")
        path = []

        for i in subArr:
            if i != self.endIndex:
                cost, subPath = self.tsp(subArr, i)
                cost += self.Dist[v][i]
                if cost < minCost:
                    minCost = cost
                    path = [v] + subPath
        return minCost, path
