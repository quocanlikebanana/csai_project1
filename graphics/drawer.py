from component.point import Point
from graphics.graphics import Graphics  # Because name conflict
from graphics.color import *
from component.enviroment import Enviroment


class Drawer:
    def __init__(self, env: Enviroment, runAlgorithmOnce) -> None:
        self.env = env
        self.polycolors = genRandomDistinctColor(len(self.env.polygons))
        self.graphics = Graphics(env, self.runDraw, runAlgorithmOnce)
        self.graphics.runRender()

    def runDraw(self):
        # Order decides
        self.drawMapBorder()
        self.drawPolygons()
        self.drawPickupPoints()
        self.drawOpened()
        self.drawClosed()
        self.drawDone()
        self.drawStartEndPoint()
        self.graphics.renderGrid(BASE_COLOR["BLACK"])  # Draw this last to avoid overlap
        # Có thể cải tiến render đồng bộ

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
            self.graphics.renderSymbolPixel(p, "x")
