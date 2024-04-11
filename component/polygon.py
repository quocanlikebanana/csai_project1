from component.moving import MovingPoint, VeloOrbit
from component.point import Vector, Point

FILL_POLYGON = False


class Polygon:
    def __init__(self, vertices: list[Point], orbit: VeloOrbit = None):
        self.vertices: list[Point] = []
        if validate(vertices):
            self.vertices = vertices
        else:
            raise ValueError("invalid vertices")
        self.edges: list[Vector] = []
        self.internalPoints: list[Point] = []
        self.movingVertices: list[MovingPoint] = []
        self.orbit = orbit
        self._updateTranslates()
        self._updateEdges()
        self._updateInternalPoints()  # No need To Fill
    def __str__(self) -> str:
            tmp = ''
            for i in range(len(self.vertices)):
                tmp = tmp + self.vertices[i].__str__()+ " "
            return tmp

    @property
    def points(self):
        setEdge = set([p for e in self.edges for p in e.points])
        setIntern = set(self.internalPoints)
        return list(setEdge | setIntern)

    def _updateEdges(self):
        self.edges.clear()
        vLen = len(self.vertices)
        for i in range(0, vLen):
            vec = Vector(self.vertices[i - 1], self.vertices[i])
            self.edges.append(vec)

    def _updateInternalPoints(self):
        self.internalPoints.clear()

        # Since its a polygon so max/min point are all a vertex
        max_y = max(self.vertices, key=lambda x: x.y).y
        min_y = min(self.vertices, key=lambda x: x.y).y

        # Handle vertices and edge
        lEdge = len(self.edges)
        for ie in range(lEdge):
            cur = self.edges[ie]
            # straight line
            if cur.getY() == 0:
                iback = 1
                while self.edges[ie - iback].getY() == 0 and abs(ie - iback) < lEdge:
                    iback += 1
                ifoward = 1
                while (
                    self.edges[(ie + ifoward) % lEdge].getY() == 0
                    and abs(ie - ifoward) < lEdge
                ):
                    ifoward += 1
                pre = self.edges[ie - iback]
                next = self.edges[(ie + ifoward) % lEdge]
                if pre.getY() * next.getY() > 0:
                    next.cutYStart()
                cur.clearPoints()
            # case "<": remove 1 point
            else:
                revpre = self.edges[ie - 1].reverse()
                if cur.getY() * revpre.getY() < 0:
                    cur.cutYStart()

        # Ordering Projection
        xProjByY_MaxMin: dict[int, list[int]] = {}
        yValues = range(min_y, max_y + 1)
        for y in yValues:
            xProjByY_MaxMin[y] = []
            intersects: list[list[Point]] = []
            # arrange by min then get max / min alternatively
            for e in self.edges:
                intersect: list[int] = e.X_intersect_Y(y)
                if intersect != None:
                    intersect.sort()
                    intersects.append(intersect)
            intersects.sort(key=lambda x: x[0])
            takeMax = True
            for its in intersects:
                if takeMax:
                    xProjByY_MaxMin[y].append(max(its))
                else:
                    xProjByY_MaxMin[y].append(min(its))
                takeMax = not takeMax

        # Filling
        for y in xProjByY_MaxMin:
            lIntersects = len(xProjByY_MaxMin[y])
            if lIntersects % 2 != 0:
                raise Exception()
            for i in range(0, lIntersects, 2):
                if xProjByY_MaxMin[y][i] + 1 < xProjByY_MaxMin[y][i + 1]:
                    for x in range(
                        xProjByY_MaxMin[y][i] + 1, xProjByY_MaxMin[y][i + 1]
                    ):
                        self.internalPoints.append(Point(x, y))
        pass

    def _updateTranslates(self):
        # translates = self.orbit.getOrbit() # Will cause error because same reference to orbit
        if self.orbit != None:
            for v in self.vertices:
                self.movingVertices.append(MovingPoint(v, self.orbit.getOrbit()))
        pass

    # when speed is applied

    # this will change states to creates the feeling of being blocked
    def getPesudoMoving(self) -> list[Point]:
        if self.orbit == None:
            return self.vertices.copy()
        pesudoMoveVertices: list[Point] = []
        for mv in self.movingVertices:
            mv.move()
            p = mv.getPoint()
            pesudoMoveVertices.append(p)
        return pesudoMoveVertices

    def move(self, pesudoMoveVertices):
        self.vertices.clear()
        self.vertices = pesudoMoveVertices
        self._updateEdges()
        self._updateInternalPoints()
        pass


# False:
# Two adjacent points is identical
# Less than 3 vertices
def validate(vertices: list[Point]):
    lenVer = len(vertices)
    if lenVer < 3:
        return False
    for i in range(1, lenVer):
        if vertices[i].x == vertices[i - 1].x and vertices[i].y == vertices[i - 1].y:
            return False
    return True
