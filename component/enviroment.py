from enum import Enum
from component.map import CELL_STATE, Cell
from component.point import Point, Vector
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
        self.startPoint: Point = startPoint
        self.endPoint: Point = endPoint
        # PickupPoint id is also the index
        self.pickupPoints: list[Point] = pickupPoints
        # Polygon id is also the index, border has index of 0
        self.polygons: dict[int, Polygon] = {}
        for id, poly in enumerate(polygons):
            self.polygons[id] = poly
        self.polyPoints: list[Point] = []
        self.borderPoints: list[Point] = []
        self._updatePolyPoints()
        self._updateBorderPoints()
        self._validateEnv()
        ## ====
        ## After this, the enviroment is valid
        self.blockPoints: list[Point] = []
        self._updateBlockPoints()
        self.map = [
            [Cell(Point(x, y), CELL_STATE.NONE) for y in range(nrow)]
            for x in range(ncol)
        ]
        self._updateMap()
        self.openedPoints: list[Point] = []
        self.closedPoints: list[Point] = []
        self.donePoints: list[Point] = []

    def _updateMap(self):
        self.map[self.startPoint.x][self.startPoint.y]._state = CELL_STATE.START
        self.map[self.endPoint.x][self.endPoint.y]._state = CELL_STATE.END
        for p in self.pickupPoints:
            self.map[p.x][p.y].setState(CELL_STATE.PICKUP)
        for p in self.borderPoints:
            self.map[p.x][p.y].setState(CELL_STATE.BLOCKED, None)
        for id in self.polygons:
            for p in self.polygons[id].points:
                self.map[p.x][p.y].setState(CELL_STATE.BLOCKED, id)
        pass

    def _updatePolyPoints(self):
        self.polyPoints = set([p for po in self.polygons.values() for p in po.points])
        self._updateBlockPoints()

    def _updateBlockPoints(self):
        setPoly = set(self.polyPoints)
        setBorder = set(self.borderPoints)
        self.blockPoints = list(set(setPoly | setBorder))
        pass

    def _updateBorderPoints(self):
        for x in range(0, self.ncol):
            self.borderPoints.append(Point(x, 0))
            self.borderPoints.append(Point(x, self.nrow - 1))
        for y in range(0, self.nrow):
            self.borderPoints.append(Point(0, y))
            self.borderPoints.append(Point(self.ncol - 1, y))
        self._updateBlockPoints()

    def updateMovement(self):
        for id in self.polygons:
            pmv = self.polygons[id].getPesudoMoving()
            if self.validatePolygonVertices(pmv, self.polygons[id]):
                for p in self.polygons[id].points:
                    self.map[p.x][p.y].setState(CELL_STATE.NONE)
                self.polygons[id].move(pmv)
                for p in self.polygons[id].points:
                    self.map[p.x][p.y].setState(CELL_STATE.BLOCKED, id)
        self._updatePolyPoints()

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

    # vertices might not from polygon, it could be pesudo ones
    def validatePolygonVertices(self, vertices: list[Point], polygon: Polygon) -> bool:
        testEdgePoints: list[Point] = []
        vLen = len(vertices)
        for i in range(0, vLen):
            vec = Vector(vertices[i - 1], vertices[i])
            for p in vec.points:
                testEdgePoints.append(p)
        for v in testEdgePoints:
            if not self._checkInRange(v):
                return False
            # Check for crossed polygon
            otherPolyPoints = [
                point
                for expoly in self.polygons.values()
                if expoly != polygon
                for point in expoly.points
            ]
            if v in otherPolyPoints:
                return False
        return True

    def _validateEnv(self):
        if not self.validatePosition(self.startPoint) or not self.validatePosition(
            self.endPoint
        ):
            raise ValueError("invalid startpont / endpoint")
        for poly in self.pickupPoints:
            if not self.validatePosition(poly):
                raise ValueError("invalid pickup points")
        for poly in self.polygons.values():
            if self.validatePolygonVertices(poly.vertices, poly) == False:
                raise ValueError("invalid polygons")
        return True

    def validatePosition(self, pos: Point):
        if self._checkInRange(pos) and self._checkNotOnPolygon(pos):
            return True
        return False
