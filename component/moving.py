from component.map import DIRECTION
from component.point import Point


# velocity is pixel moved per tick


class VeloTranslate:
    def __init__(self, vx: float, vy: float, time: float) -> None:
        self._vx = vx
        self._vy = vy
        self.time = time
        self.progress = time
        pass

    def getV(self) -> tuple[float, float]:
        if self.progress <= 0:
            raise ValueError()
        self.progress -= 1  # moved vx, vy pixel on 1 tick
        return self._vx, self._vy

    def reloadProgress(self):
        self.progress = self.time

    def isDone(self) -> bool:
        return self.progress <= 0


## Woulddo: if current translate dont work
class TimeTranslate:
    def __init__(self, dir: DIRECTION, time: float, numberOfMoves) -> None:
        self.dir = dir
        self.time = time
        self.numberOfMoves = numberOfMoves
        self.progress = numberOfMoves
        pass

    def getV(self) -> tuple[float, float]:
        if self.progress <= 0:
            raise ValueError()
        self.progress -= 1  # moved vx, vy pixel on 1 tick
        return self.dir.value.x, self.dir.value.y

    def reloadProgress(self):
        self.progress = self.numberOfMoves

    def isDone(self) -> bool:
        return self.progress <= 0


class MovingPoint:
    def __init__(self, point: Point, translates: list[VeloTranslate]) -> None:
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


class VeloOrbit:
    def __init__(self, veloAndTimeList: list[tuple[float, float, float]]) -> None:
        self._vt = veloAndTimeList

    # We need to copy out the array or all points will reference to the same array
    def getOrbit(self) -> list[VeloTranslate]:
        orbit: list[VeloTranslate] = []
        lp = len(self._vt)
        if lp > 1:
            for i in range(lp):
                orbit.append(
                    VeloTranslate(self._vt[i][0], self._vt[i][1], self._vt[i][2])
                )
        return orbit


### Below are trash
### Below are trash
### Below are trash
### Below are trash
### Below are trash


# class Translate:
#     def __init__(self, start: Point, end: Point, time: float) -> None:
#         self.vx = (end.x - start.x) / time
#         self.vy = (end.y - start.y) / time
#         self.time = time
#         self.progress = time
#         pass

#     def getV(self) -> tuple[float, float]:
#         if self.progress <= 0:
#             raise ValueError()
#         self.progress -= 1  # moved vx, vy pixel on 1 tick
#         return self.vx, self.vy

#     def reloadProgress(self):
#         self.progress = self.time

#     def isDone(self) -> bool:
#         return self.progress <= 0


# # The most stable one currently
# class LinearOrbit:
#     def __init__(self, points: list[Point], constTime: float) -> None:
#         self.points = points
#         self.constTime = constTime

#     def getOrbit(self) -> list[Translate]:
#         lp = len(self.points)
#         if lp <= 1:
#             return []
#         orbit: list[Translate] = []
#         for i in range(lp):
#             curp = self.points[i]
#             nexp = self.points[(i + 1) % lp]
#             orbit.append(Translate(curp, nexp, self.constTime))
#         return orbit


# # Ratio is blocks moved when algorithm run once ~~ velocity
# # The smaller, the more acurrate
# # Bigger than 1 or not divisible by the distance will lead to off orbit
# class RatioOrbit:
#     def __init__(self, points: list[Point], timeRatio: float) -> None:
#         self.points = points
#         self.timeRatio = timeRatio

#     def getOrbit(self) -> list[Translate]:
#         lp = len(self.points)
#         if lp <= 1 or self.timeRatio == 0:
#             return []
#         orbit: list[Translate] = []
#         for i in range(lp):
#             curp = self.points[i]
#             nexp = self.points[(i + 1) % lp]
#             time = float(curp.getMattathanDistance(nexp) / self.timeRatio)
#             orbit.append(Translate(curp, nexp, time))
#         return orbit


# # Glitchy
# # Offorbit all the time
# class ConstantOrbit:
#     def __init__(self, points: list[Point], totalTime: float) -> None:
#         self.points = points
#         self.totalTime = totalTime

#     def getOrbit(self) -> list[Translate]:
#         lp = len(self.points)
#         if lp <= 1:
#             return []
#         totalDistance = 0
#         for i in range(lp):
#             curp = self.points[i]
#             nexp = self.points[(i + 1) % lp]
#             totalDistance += curp.getAbsDistance(nexp)
#         orbit: list[Translate] = []
#         for i in range(lp):
#             curp = self.points[i]
#             nexp = self.points[(i + 1) % lp]
#             time = (curp.getAbsDistance(nexp) / totalDistance) * self.totalTime
#             orbit.append(Translate(curp, nexp, time))
#         return orbit
