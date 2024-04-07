from enum import Enum
from algorithm.algorithm import Algorithm


class METHODS(Enum):
    LEFT = 1
    LEFT_UP = 2
    UP = 3
    RIGHT_UP = 4
    RIGHT = 5
    RIGHT_DOWN = 6
    DOWN = 7
    LEFT_DOWN = 8


class DJK_Node:

    pass


class Dijkstra(Algorithm):
    def __init__(self, env) -> None:
        super().__init__(env)

    def searchOnce(self):
        pass

    pass
