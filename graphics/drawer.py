from component.map import CELL_STATE, Cell
from component.point import Point
from graphics.graphics import Graphics  # Because name conflict
from graphics.color import *
from component.environment import Environment


class Drawer:
    def __init__(self, env: Environment) -> None:
        self.env = env
        self.polycolors = genRandomDistinctColor(len(self.env.polygons))
        # self.graphics = Graphics(env, self.drawAll)
        self.graphics = Graphics(env, self.drawAll)

    def run(self):
        return self.graphics.run()

    # Old draw function
    def drawAll(self):
        # Order decides
        self.drawMapBorder()
        self.drawPickupPoints()
        self.drawOpened()
        self.drawClosed()
        self.drawPolygons()
        self.drawDone()
        self.drawStartEndPoint()
        self.drawAgent(self.env.agentPoint)
        self.graphics.renderGrid(BASE_COLOR["BLACK"])  # Draw this last to avoid overlap

    def drawAllByMap(self):
        for x in range(self.env.ncol):
            for y in range(self.env.nrow):
                self.switchPixelDraw(self.env.map[x][y])
        self.drawOverlayInit()

    def drawOverlayInit(self):
        self.drawStartPixel(self.env.startPoint)
        self.drawEndPixel(self.env.endPoint)
        for p in self.env.pickupPoints:
            self.drawPickupPixel(p)
        for s in self.env.charOverlay:
            self.graphics.renderSymbolPixel(s[0], s[1])
        self.graphics.renderGrid(BASE_COLOR["BLACK"])  # Draw this last to avoid overlap
        self.drawAgent(self.env.agentPoint)
        pass

    def switchPixelDraw(self, cell: Cell):
        state = cell.getState()[0]
        if state == CELL_STATE.BLOCKED:
            self.drawBlockPixel(cell.point, cell.getState()[1])
        elif state == CELL_STATE.OPEN:
            self.drawOpenPixel(cell.point)
        elif state == CELL_STATE.CLOSE:
            self.drawClosePixel(cell.point)
        elif state == CELL_STATE.DONE:
            self.drawDonePixel(cell.point)
        pass

    def drawStartPixel(self, point: Point):
        self.graphics.renderFilledPixel(point, BASE_COLOR["BLUE"])
        self.graphics.renderSymbolPixel(point, "S")
        pass

    def drawEndPixel(self, point: Point):
        self.graphics.renderFilledPixel(point, BASE_COLOR["PINK"])
        self.graphics.renderSymbolPixel(point, "E")
        pass

    def drawPickupPixel(self, point: Point):
        self.graphics.renderFilledPixel(point, BASE_COLOR["TEAL"])
        pass

    def drawBlockPixel(self, point: Point, id=None):
        if id == None:
            self.graphics.renderFilledPixel(point, BASE_COLOR["GRAY"])
        else:
            self.graphics.renderFilledPixel(
                point, self.polycolors[id % len(self.polycolors)]
            )
        pass

    def drawOpenPixel(self, point: Point):
        self.graphics.renderFilledPixel(point, BASE_COLOR["GREEN"])
        pass

    def drawClosePixel(self, point: Point):
        self.graphics.renderFilledPixel(point, BASE_COLOR["RED"])
        pass

    def drawDonePixel(self, point: Point):
        self.graphics.renderFilledPixel(point, BASE_COLOR["YELLOW"])
        self.graphics.renderSymbolPixel(point, "+")
        pass

    def drawAgent(self, point: Point):
        if point == None:
            return
        self.graphics.renderFilledPixel(point, BASE_COLOR["GREEN"])
        self.graphics.renderSymbolPixel(point, "A")
        pass

    # Old
    # Old
    # Old
    # Old
    # Old
    # Old

    def drawMapBorder(self):
        for p in self.env.borderPoints:
            self.graphics.renderFilledPixel(p, BASE_COLOR["GRAY"])

    def drawStartEndPoint(self):
        self.graphics.renderFilledPixel(self.env.startPoint, BASE_COLOR["BLUE"])
        self.graphics.renderSymbolPixel(self.env.startPoint, "S")
        self.graphics.renderFilledPixel(self.env.endPoint, BASE_COLOR["PINK"])
        self.graphics.renderSymbolPixel(self.env.endPoint, "E")

    def drawPickupPoints(self):
        i = 0
        for p in self.env.pickupPoints:
            i += 1
            self.graphics.renderFilledPixel(p, BASE_COLOR["TEAL"])
            self.graphics.renderSymbolPixel(p, str(i))

    def drawPolygons(self):
        for i in range(len(self.env.polygons)):
            fullPoints = self.env.polygons[i].points
            for p in fullPoints:
                self.graphics.renderFilledPixel(
                    p, self.polycolors[i % len(self.polycolors)]
                )

    def drawOpened(self):
        for p in self.env.openedPoints:
            self.graphics.renderFilledPixel(p, BASE_COLOR["GREEN"])

    def drawClosed(self):
        for p in self.env.closedPoints:
            self.graphics.renderFilledPixel(p, BASE_COLOR["RED"])

    def drawDone(self):
        for p in self.env.donePoints:
            self.graphics.renderFilledPixel(p, BASE_COLOR["YELLOW"])
            self.graphics.renderSymbolPixel(p, "+")
