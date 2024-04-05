from component.point import Vector, Point


class Polygon:
    def __init__(self, vertices: list[Point]):
        self.vertices: list[Point] = []
        if validate(vertices):
            self.vertices = vertices
        else:
            raise ValueError("invalid vertices")
        self.edges: list[Vector] = []
        self.internalPoints: list[Point] = []
        self.updateEdges()
        self.updateInternalPoints()

    @property
    def points(self):
        setEdge = set([p for e in self.edges for p in e.points])
        setIntern = set(self.internalPoints)
        return list(setEdge | setIntern)

    def updateEdges(self):
        vLen = len(self.vertices)
        for i in range(0, vLen):
            vec = Vector(self.vertices[i - 1], self.vertices[i])
            self.edges.append(vec)

    def updateInternalPoints(self):
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

        # for y in xProjByY_MaxMin:
        #     addPoint = None
        #     addFlag = False
        #     for x in range(min_x, max_x + 1):
        #         if addFlag == True:
        #             self.internalPoints.append(Point(x, y))
        #         if addPoint != None and x == addPoint:
        #             self.internalPoints.append(Point(x, y))
        #         if x == xProjByY_MaxMin[y]
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


# def getLinePoints_YProj_intern(pStart: Point, pEnd: Point) -> list[Point]:
#     vertices = getLinePoints(pStart, pEnd)
#     slope, intercept = getSlopeAndIntercept(pStart, pEnd)
#     if slope == 0:
#         return []
#     vertices.sort(key=lambda x: x.y)
#     rangeY = range(vertices[0].y, vertices[-1].y + 1)
#     verticesResult: list[Point] = []
#     for y in rangeY:
#         bufferX: list[int] = []
#         while len(vertices) > 0:
#             if vertices[0].y == y:
#                 bufferX.append(vertices[0].x)
#                 vertices.pop(0)
#             else:
#                 break
#         if slope > 0:
#             verticesResult.append(Point(min(bufferX), y))
#         else:
#             verticesResult.append(Point(max(bufferX), y))
#     return verticesResult


# def getHorizontalIntersection(pStart: Point, pEnd: Point, y: int):
#     slope, intercept = getSlopeAndIntercept(pStart, pEnd)
#     if slope == 0:
#         if pStart.y == y:
#             return 2, pStart
#         return 0, None
#     if slope == inf:
#         if min(pStart.y, pEnd.y) <= y and y <= max(pStart.y, pEnd.y):
#             return 1, Point(pStart.x, y)
#         return 0, None

#     intersection_x = math.ceil((y - intercept) / slope)
#     if min(pStart.x, pEnd.x) <= intersection_x and intersection_x <= max(
#         pStart.x, pEnd.x
#     ):
#         return 1, Point(intersection_x, y)
#     return 0, None
