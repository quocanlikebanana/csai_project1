from enum import Enum
from component.map import CELL_STATE, DIRECTION, Cell, StateTrigger
from component.point import Point, Vector
from component.polygon import Polygon

CHECK_POLYGON_MOVE = False


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
        self.validateEnv()
        ## ====
        ## After this, the enviroment is valid
        self.moving = False
        for p in self.polygons:
            if self.polygons[p].orbit != None:
                self.moving = True
                break
        self.blockPoints: list[Point] = []
        self._updateBlockPoints()
        self.map = [[Cell(Point(x, y)) for y in range(nrow)] for x in range(ncol)]
        self._updateMap()
        self.openedPoints: list[Point] = []
        self.closedPoints: list[Point] = []
        self.donePoints: list[Point] = []
        ## Update
        self._stateTrigger = None
        self._frontier = []
        self._explored = []

    # these points are not managed by env or changeable
    def _updateMap(self):
        self.map[self.startPoint.x][self.startPoint.y].setStateWithTrigger(
            CELL_STATE.START
        )
        self.map[self.endPoint.x][self.endPoint.y].setStateWithTrigger(CELL_STATE.END)
        for p in self.pickupPoints:
            self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.PICKUP)
        for p in self.borderPoints:
            self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.BLOCKED)
        for id in self.polygons:
            for p in self.polygons[id].points:
                self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.BLOCKED, extraInfo=id)
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

    def injectTrigger(self, stateTriggers: list[StateTrigger]):
        for c in self.map:
            for r in c:
                r.setTriggers(stateTriggers)
        pass

    def moveAllPolygons(self):
        # Still slower even when no validating
        if self.moving == True:
            for id in self.polygons:
                pmv = self.polygons[id].getPesudoMoving()
                ## New way of validating:
                # check if point on map is in other polygon instead
                if CHECK_POLYGON_MOVE == False or self.validatePolygonVertices(
                    pmv, self.polygons[id]
                ):
                    for p in self.polygons[id].points:
                        self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.NONE)
                    self.polygons[id].move(pmv)
                    for p in self.polygons[id].points:
                        self.map[p.x][p.y].setStateWithTrigger(
                            CELL_STATE.BLOCKED, extraInfo=id
                        )
            self._updatePolyPoints()

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

    def validateEnv(self):
        if not self.validatePositionByList(
            self.startPoint
        ) or not self.validatePositionByList(self.endPoint):
            raise ValueError("invalid startpont / endpoint")
        for poly in self.pickupPoints:
            if not self.validatePositionByList(poly):
                raise ValueError("invalid pickup points")
        for poly in self.polygons.values():
            if self.validatePolygonVertices(poly.vertices, poly) == False:
                raise ValueError("invalid polygons")
        return True

    def validatePositionByList(self, pos: Point):
        if self._checkInRange(pos) and self._checkNotOnPolygon(pos):
            return True
        return False

    def clearFinding(self):
        allFindingPoints = self.closedPoints + self.openedPoints
        for p in allFindingPoints:
            self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.NONE)
        self.closedPoints.clear()
        self.openedPoints.clear()
        pass

    def appendClosePoint(self, p: Point):
        if self.map[p.x][p.y].getState()[0] != CELL_STATE.CLOSE:
            self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.CLOSE, self.closedPoints)
        pass

    def appendOpenPoint(self, p: Point):
        if self.map[p.x][p.y].getState()[0] != CELL_STATE.OPEN:
            self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.OPEN, self.openedPoints)
        pass

    def appendDonePoint(self, p: Point):
        if self.map[p.x][p.y].getState()[0] != CELL_STATE.DONE:
            self.map[p.x][p.y].setStateWithTrigger(CELL_STATE.DONE, self.donePoints)
        pass

    def validatePositionByMap(self, pos: Point):
        if (
            self._checkInRange(pos)
            and self.map[pos.x][pos.y].getState()[0] != CELL_STATE.BLOCKED
        ):
            return True
        return False

    def validatePathMove(self, pos: Point, dir: DIRECTION):
        dest = pos.relative(dir.value.x, dir.value.y)
        if (
            self.validatePositionByMap(dest) == False
            or self.map[dest.x][dest.y].getState()[0] == CELL_STATE.CLOSE
            or self.map[dest.x][dest.y].getState()[0] == CELL_STATE.OPEN
        ):
            return False
        if DIRECTION.isCrossDir(dir) == True:
            hor = self.map[pos.x + dir.value.x][pos.y].getState()
            ver = self.map[pos.x][pos.y + dir.value.y].getState()
            if (
                hor[0] == CELL_STATE.BLOCKED
                and ver[0] == CELL_STATE.BLOCKED
                and hor[1] == ver[1]
            ):
                return False

        return True

    # Để xóa điểm theo tọa độ (value) với độ phức tạp O(1) mà vẫn giữ
    # tính chất của dslk thì chỉ có định nghĩa lại list
