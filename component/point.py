from math import inf
import math


class Point:
    def __init__(self, x: int, y: int):
        self.x = int(x) or 0
        self.y = int(y) or 0

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


class Vector:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.points: list[Point] = []
        self.slope: int = None
        self.intercept: int = None
        self._init()
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
    def _init(self):
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


# velocity is pixel moved per tick
class Translate:
    def __init__(self, start: Point, end: Point, time: float) -> None:
        self.vx = (end.x - start.x) / time
        self.vy = (end.y - start.y) / time
        self.time = time
        self.progress = time
        pass

    def getV(self) -> tuple[float, float]:
        if self.progress <= 0:
            raise ValueError()
        self.progress -= 1  # moved vx, vy pixel on 1 tick
        return self.vx, self.vy

    def reloadProgress(self):
        self.progress = self.time

    def isDone(self) -> bool:
        return self.progress <= 0


class ConstantOrbit:
    def __init__(self, points: list[Point], totalTime: float) -> None:
        self.points = points
        self.totalTime = totalTime

    def getOrbit(self) -> list[Translate]:
        lp = len(self.points)
        if lp <= 1:
            return []
        totalDistance = 0
        for i in range(lp):
            curp = self.points[i]
            nexp = self.points[(i + 1) % lp]
            totalDistance += curp.getAbsDistance(nexp)
        orbit: list[Translate] = []
        for i in range(lp):
            curp = self.points[i]
            nexp = self.points[(i + 1) % lp]
            time = (curp.getAbsDistance(nexp) / totalDistance) * self.totalTime
            orbit.append(Translate(curp, nexp, time))
        return orbit


class MovingPoint:
    def __init__(self, point: Point, translates: list[Translate]) -> None:
        self.translates = translates
        self.x = float(point.x)
        self.y = float(point.y)
        self.curTransId = 0

    def move(self):
        lTranslate = len(self.translates)
        while self.translates[self.curTransId].isDone():
            self.translates[self.curTransId].reloadProgress()
            self.curTransId = (self.curTransId + 1) % lTranslate
        translate = self.translates[self.curTransId]
        vx, vy = translate.getV()
        self.x = self.x + vx
        self.y = self.y + vy

    def getPoint(self) -> Point:
        return Point(int(self.x), int(self.y))
