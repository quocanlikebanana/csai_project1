from enum import Enum
from component.enviroment import Enviroment


class CELL_STATS(Enum):
    BLOCKED = 1
    OPEN = 2
    CLOSE = 3
    START = 4
    END = 5
    NONE = 6
    DONE = 7


class Map:
    def __init__(self, env: Enviroment) -> None:
        self.env = env
        self.gridXY: list[list[CELL_STATS]] = []
        pass

    def _updateMap(self):
        for _ in range(self.env.ncol):
            col = []
            for _ in range(self.env.nrow):
                col.append(CELL_STATS.NONE)
            self.gridXY.append(col)
        bps = self.env.blockPoints
        for p in bps:
            self.nodes[p.x][p.y].status = CELL_STATS.BLOCKED
