from component.enviroment import Enviroment
from component.map import CELL_STATE
from component.point import Point
import heapq


class Dijkstra:
    def __init__(self, env: Enviroment) -> None:
        self.env = env
        self.open: list[(float, Point)] = [(0, env.startPoint)]
        self.shortest_path: {Point, list[Point]} = {env.startPoint: [env.startPoint]}
        self.distances: {Point, float} = {env.startPoint: 0}
        self.searching = True

    def searchOnce(self):
        if self.searching == False:
            return False
        else:
            if not self.open:
                raise ValueError("Dijkstra not found")

            current_point: Point
            current_distance, current_point = heapq.heappop(self.open)

            if current_point == self.env.endPoint:
                self.env.donePoints = self.shortest_path[self.env.endPoint]
                self.searching = False

            for i in range(-1, 2):
                for j in range(-1, 2):
                    adjacent_point: Point = current_point.relative(i, j)

                    if (
                        self.env.validatePosition(adjacent_point)
                        and self.env.map[adjacent_point.x][adjacent_point.y].getState()[
                            0
                        ]
                        != CELL_STATE.CLOSE
                    ):
                        distance = current_distance + current_point.getAbsDistance(
                            adjacent_point
                        )
                        if distance < self.distances.get(adjacent_point, float("inf")):
                            self.distances[adjacent_point] = distance
                            heapq.heappush(self.open, (distance, adjacent_point))
                            self.shortest_path[adjacent_point] = self.shortest_path[
                                current_point
                            ] + [adjacent_point]
                            self.env.openedPoints.append(adjacent_point)
            self.env.closedPoints.append(current_point)
            self.env.map[current_point.x][current_point.y].setState(CELL_STATE.CLOSE)
            return True
