from component.point import Point


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


class LinearOrbit:
    def __init__(self, points: list[Point], constTime: float) -> None:
        self.points = points
        self.constTime = constTime

    def getOrbit(self) -> list[Translate]:
        lp = len(self.points)
        if lp <= 1:
            return []
        orbit: list[Translate] = []
        for i in range(lp):
            curp = self.points[i]
            nexp = self.points[(i + 1) % lp]
            orbit.append(Translate(curp, nexp, self.constTime))
        return orbit


# Ratio is blocks moved when algorithm run once ~~ velocity
# The smaller, the more acurrate
# Bigger than 1 or not divisible by the distance will lead to off orbit
class RatioOrbit:
    def __init__(self, points: list[Point], timeRatio: float) -> None:
        self.points = points
        self.timeRatio = timeRatio

    def getOrbit(self) -> list[Translate]:
        lp = len(self.points)
        if lp <= 1 or self.timeRatio == 0:
            return []
        orbit: list[Translate] = []
        for i in range(lp):
            curp = self.points[i]
            nexp = self.points[(i + 1) % lp]
            time = float(curp.getMattathanDistance(nexp) / self.timeRatio)
            orbit.append(Translate(curp, nexp, time))
        return orbit


# Glitchy
# Offorbit all the time
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
        if lTranslate < 2:
            raise ValueError("orbit must have atleast 2 translate")
        while self.translates[self.curTransId].isDone():
            self.translates[self.curTransId].reloadProgress()
            self.curTransId = (self.curTransId + 1) % lTranslate
        translate = self.translates[self.curTransId]
        vx, vy = translate.getV()
        self.x = self.x + vx
        self.y = self.y + vy

    def getPoint(self) -> Point:
        return Point(round(self.x), round(self.y))
