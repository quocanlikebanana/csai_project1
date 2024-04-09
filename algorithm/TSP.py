from enum import Enum
import math
import copy
from algorithm.priorityqueue import PriorityQueue
from component.enviroment import Enviroment
from component.point import Point


BLOCK_SIZE = 10
CROSS_COST = 15
STRAIGHT_COST = 10


def EuclideanHeuristic(curNode, targetNode):
    cost = CROSS_COST
    if curNode.x - targetNode.x == 0 or curNode.y - targetNode.y == 0 :
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


class Edge:
    def __init__(self,nodes,cost,vertex):
        self.nodes = []
        self.vertex = []
        self.cost = cost
        

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



def FindEdge(nodes,map):
    Edge = []
    for node in nodes:
        return
        
 
        
def Astar(map: AS_Map,startPoint,endPoint,heuristicFunction):
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
            searching = False
            currentNode.status = NodeStatus.END
            while currentNode.parent != startNode:
                currentNode.parent.status = NodeStatus.DONE
                cost +=  currentNode.parent.f
                nodeArr.append(currentNode.parent)
                currentNode = currentNode.parent
        else:
            Neighbours = []
            Neighbours = map.GetNeighbours(currentNode)
            
            for node in Neighbours:
                node.parent = currentNode
                node.h = heuristicFunction(node, targetNode)
                node.f = node.g + node.h
                node.status = NodeStatus.OPEN
                open.insert(node)
    return nodeArr,cost
        


class TSP:
    def __init__(self, env, heuristicFunction) -> None:
        self.map = AS_Map(env)
        self.listV = []
        self.listV.append(self.map.nodes[env.startPoint.x][env.startPoint.y])
        for point in self.map.env.pickupPoints:
            self.listV.append(self.map.nodes[point.x][point.y])
        self.listV.append(self.map.nodes[self.map.env.endPoint.x][self.map.env.endPoint.y])
        self.heuristicFunction = heuristicFunction
        self.searching = True
        self.Edge = []

    def searchOnce(self):
        if self.searching:
            for i in range(len(self.listV) - 1):
                for j in range(i+ 1,len(self.listV)):
                    mapCopy = copy.deepcopy(self.map)
                    nodes,cost = Astar(mapCopy,self.listV[i],self.listV[j],self.heuristicFunction)
                    self.Edge.append(Edge(nodes,cost,[self.listV[i],self.listV[j]]))
            
            print(len(self.Edge))  
            self.searching = False  
        else:
            return True
        
        
        # if self.searching == False:
        #     return False
        # else:
        #     if self.open.isEmpty():
        #         raise ValueError("astar not found")
        #     currentNode = self.open.delete()
        #     self.close.insert(currentNode)
        #     if currentNode != self.startNode:
        #         currentNode.status = NodeStatus.CLOSE
        #         self.map.env.closedPoints.append(Point(currentNode.x, currentNode.y))
        #     if currentNode == self.targetNode:
        #         self.searching = False
        #         # print(currentNode.f)
        #         currentNode.status = NodeStatus.END
        #         while currentNode.parent != self.startNode:
        #             currentNode.parent.status = NodeStatus.DONE
        #             self.map.env.donePoints.append(
        #                 Point(currentNode.parent.x, currentNode.parent.y)
        #             )
        #             currentNode = currentNode.parent
        #     else:
        #         Neighbours = []
        #         Neighbours = self.map.GetNeighbours(currentNode)
        #         for node in Neighbours:
        #             node.parent = currentNode
        #             node.h = self.heuristicFunction(node, self.targetNode)
        #             node.f = node.g + node.h
        #             node.status = NodeStatus.OPEN
        #             self.map.env.openedPoints.append(Point(node.x, node.y))
        #             self.open.insert(node)
        #     return True
    
   
