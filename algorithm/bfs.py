from component.environment import Environment
from component.map import CELL_STATE
from component.point import Point
from queue import Queue

CROSS_COST = 2**0.5
STRAIGHT_COST = 1


class BFS:
    def __init__(self, env: Environment) -> None:
        self.env = env
        self.open: Queue[list[Point]] = Queue()
        self.open.put([env.startPoint])
        # self.close = env.close
        self.searching = True

    def searchOnce(self):
        if self.searching == False:
            return False
        else:
            if self.open.empty():
                self.searching = False
                raise ValueError("BFS not found")

            cur_path = self.open.get()
            final_point = cur_path[-1]

            # go up
            self.path_extend(cur_path, final_point, 0, 1)
            # go down
            self.path_extend(cur_path, final_point, 0, -1)
            # go left
            self.path_extend(cur_path, final_point, -1, 0)
            # go right
            self.path_extend(cur_path, final_point, 1, 0)
            # go upright
            self.path_extend(cur_path, final_point, -1, 1)
            # go upleft
            self.path_extend(cur_path, final_point, -1, -1)
            # go downright
            self.path_extend(cur_path, final_point, 1, 1)
            # go downleft
            self.path_extend(cur_path, final_point, 1, -1)

            self.env.closedPoints.append(final_point)
            self.env.map[final_point.x][final_point.y].setState(CELL_STATE.CLOSE)
            return True

    def path_extend(self, cur_path, final_point: Point, directionX, directionY):
        relative_point = final_point.relative(directionX, directionY)

        if relative_point == self.env.endPoint:
            self.env.donePoints = cur_path + [relative_point]
            self.searching = False

            cost = 0
            for i in range(1, len(self.env.donePoints)):
                cost = cost + (
                    1
                    if self.env.donePoints[i].x == self.env.donePoints[i - 1].x
                    or self.env.donePoints[i].y == self.env.donePoints[i - 1].y
                    else 2**0.5
                )

            print(f"Cost: {cost}")
        # todo: or or and
        elif (
            self.env.validatePositionByList(relative_point)
            and self.env.map[relative_point.x][relative_point.y].getState()[0]
            != CELL_STATE.CLOSE
            and self.env.map[relative_point.x][relative_point.y].getState()[0]
            != CELL_STATE.OPEN
        ):
            self.open.put(cur_path + [relative_point])
            self.env.openedPoints.append(relative_point)
            self.env.map[relative_point.x][relative_point.y].setState(CELL_STATE.OPEN)
