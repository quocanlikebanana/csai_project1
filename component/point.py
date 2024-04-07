from math import inf
import math


class Point:
    def __init__(self, x: int, y: int):
        self.x = int(x) or 0
        self.y = int(y) or 0
    def __str__(self) -> str:
        return f"({self.x}, {self.y}) "

    def __eq__(self, __value: object) -> bool:
        if type(__value) == Point:
            if __value.x == self.x and __value.y == self.y:
                return True
            return False
        return False

    def __hash__(self):
        return hash(self.x + self.y)

    def relative(self, x: int, y: int):
        return Point(self.x + x, self.y + y)

    def getAbsDistance(self, dest) -> float:
        return math.sqrt((dest.x - self.x) ** 2 + (dest.y - self.y) ** 2)

    def getMattathanDistance(self, dest) -> float:
        return abs((dest.x - self.x) + (dest.y - self.y))


class Vector:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.points: list[Point] = []
        self.slope: int = None
        self.intercept: int = None
        self._update()
        self.draftStart = start
        self.draftPoints = self.points.copy()

    def reverse(self):
        return Vector(self.end, self.start)

    def getX(self):
        return self.end.x - self.start.x

    def getY(self):
        return self.end.y - self.start.y

    # On draft

    def reset(self):
        self.draftPoints = self.points.copy()

    def cutYStart(self):
        for p in self.points:
            if p.y == self.start.y:
                self.draftPoints.remove(p)
        self.draftStart = self.draftPoints[0]

    def X_intersect_Y(self, y: int):
        # case horizontal:
        if len(self.draftPoints) == 0:
            return None
        if self.draftStart.y <= y <= self.end.y or self.end.y <= y <= self.draftStart.y:
            res = [p.x for p in self.draftPoints if p.y == y]
            if len(res) <= 0:
                raise ValueError("err intersect")
            return res
        return None

    def clearPoints(self):
        self.draftPoints.clear()

    # Init
    def _update(self):
        if self.end.y == self.start.y:
            self.slope = 0
        elif self.end.x == self.start.x:
            self.slope = inf
        else:
            self.slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        if self.slope != inf:
            self.intercept = self.start.y - self.start.x * self.slope
        if self.slope != inf:
            if abs(self.slope) <= 1:
                dir = 1 if self.start.x <= self.end.x else -1
                for x in range(self.start.x, self.end.x, dir):
                    y = round(x * self.slope + self.intercept)
                    self.points.append(Point(x, y))
            else:
                dir = 1 if self.start.y <= self.end.y else -1
                for y in range(self.start.y, self.end.y, dir):
                    x = round((y - self.intercept) / self.slope)
                    self.points.append(Point(x, y))
        else:
            dir = 1 if self.start.y <= self.end.y else -1
            for y in range(self.start.y, self.end.y, dir):
                self.points.append(Point(self.start.x, y))
        self.points.append(self.end)
