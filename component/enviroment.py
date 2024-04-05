from component.point import Point
from component.polygon import Polygon


class Enviroment:
    def __init__(
        self,
        ncol,
        nrow,
        startPoint: Point,
        endPoint: Point,
        pickupPoints: list[Point],
        polygons: list[Polygon],
    ):
        self.ncol = ncol
        self.nrow = nrow
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.pickupPoints = pickupPoints
        self.polygons = polygons
        self.borderPoints: list[Point] = []
        self._updateBorderPoints()
        self.polyPoints = set([p for po in self.polygons for p in po.points])
        if self.validateEnv() == False:
            raise ValueError(1, "invalid eviroment")
        self.blockPoints: list[Point] = []
        self._updateBlockPoints()
        self.openedPoints: list[Point] = []
        self.closedPoints: list[Point] = []
        self.donePoints: list[Point] = []

    def _updateBlockPoints(self):
        setPoly = set(self.polyPoints)
        setBorder = set(self.borderPoints)
        self.blockPoints = list(set(setPoly | setBorder))

    def _updateBorderPoints(self):
        for x in range(0, self.ncol):
            self.borderPoints.append(Point(x, 0))
            self.borderPoints.append(Point(x, self.nrow - 1))
        for y in range(0, self.nrow):
            self.borderPoints.append(Point(0, y))
            self.borderPoints.append(Point(self.ncol - 1, y))

    def update(self):
        for p in self.polygons:
            p.updateMoving()

    def _checkInRange(self, point: Point) -> bool:
        # Border is 1 pixel
        if (
            point.x > 0
            and point.x < self.ncol - 1
            and point.y > 0
            and point.y < self.nrow - 1
        ):
            return True
        return False

    def _checkNotOnPolygon(self, point: Point) -> bool:
        if point in self.polyPoints:
            return False
        return True

    def validateEnv(self):
        if not self.validatePosition(self.startPoint) or not self.validatePosition(
            self.endPoint
        ):
            return False
        for poly in self.pickupPoints:
            if not self.validatePosition(poly):
                return False
        for poly in self.polygons:
            for v in poly.vertices:
                if not self._checkInRange(v):
                    return False
                # Check crossed polygon
                otherPolyPoints = [
                    point
                    for expoly in self.polygons
                    if expoly != poly
                    for point in expoly.points
                ]
                if v in otherPolyPoints:
                    return False
        return True

    def validatePosition(self, pos: Point):
        if self._checkInRange(pos) and self._checkNotOnPolygon(pos):
            return True
        return False
