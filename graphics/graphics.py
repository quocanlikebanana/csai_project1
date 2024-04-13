import pygame
import sys
import math
import os

from component.environment import Environment
from component.point import Point
from graphics.color import BASE_COLOR

MAX_FPS = 100


class Graphics:
    def __init__(self, env: Environment, drawAll) -> None:
        self.env = env
        self.MAR_X = 30
        self.MAR_Y = 30
        self.BASE_WINDOW_HEIGHT = 600
        self.BASE_WINDOW_WIDTH = math.ceil(
            (env.ncol / env.nrow) * self.BASE_WINDOW_HEIGHT
        )
        self.FONT_SIZE = 48
        self.blocksize_x = (self.BASE_WINDOW_WIDTH - self.MAR_X * 2) / self.env.ncol
        self.blocksize_y = (self.BASE_WINDOW_HEIGHT - self.MAR_Y * 2) / self.env.nrow
        self.surface = None
        self.font = None
        self.clock = None
        self.drawAll = drawAll
        self.runAlgorithmOnce = None

    def updateBlockSize(self):
        windowWidth, windowHeight = pygame.display.get_surface().get_size()
        self.blocksize_x = (windowWidth - self.MAR_X * 2) / self.env.ncol
        self.blocksize_y = (windowHeight - self.MAR_Y * 2) / self.env.nrow

    def getScreenPosition(self, point: Point):
        windowWidth, windowHeight = pygame.display.get_surface().get_size()
        left = self.MAR_X + self.blocksize_x * point.x
        top = (
            windowHeight - self.blocksize_y * point.y - self.blocksize_y
        ) - self.MAR_Y
        return left, top

    def onEveryFrameDrawn(self):
        # self.env.updateMovement()
        if self.runAlgorithmOnce != None:
            self.runAlgorithmOnce()
            pygame.time.delay(100)
        pass

    def run(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(
            (self.BASE_WINDOW_WIDTH, self.BASE_WINDOW_HEIGHT),
            pygame.RESIZABLE,
        )
        self.font = pygame.font.Font(
            os.path.join(sys.path[0], "resources", "Lexend-Medium.ttf"), self.FONT_SIZE
        )
        pygame.display.set_caption("Path Finding")
        self.clock = pygame.time.Clock()
        polygon_move_event = pygame.USEREVENT + 1
        pygame.time.set_timer(polygon_move_event, 1000)
        self.updateBlockSize()
        # self.clock.tick(MAX_FPS)
        # Loop
        while True:
            self.surface.fill(BASE_COLOR["WHITE"])
            self.drawAll()
            self.onEveryFrameDrawn()
            pygame.display.update()
            # pygame.time.delay(200)
            # Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    # sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.updateBlockSize()
                if event.type == polygon_move_event and self.env.allowMove == True:
                    self.env.moveAllPolygons()

    def renderGrid(self, cellBorderColor) -> None:
        for x in range(0, self.env.ncol):
            for y in range(0, self.env.nrow):
                left, top = self.getScreenPosition(Point(x, y))
                rect = pygame.Rect(
                    left, top, math.ceil(self.blocksize_x), math.ceil(self.blocksize_y)
                )
                pygame.draw.rect(self.surface, cellBorderColor, rect, 1)

    def renderFilledPixel(self, point: Point, color) -> None:
        left, top = self.getScreenPosition(point)
        rect = pygame.Rect(
            left, top, math.ceil(self.blocksize_x), math.ceil(self.blocksize_y)
        )
        pygame.draw.rect(self.surface, color, rect)

    def renderSymbolPixel(self, point: Point, symbol: str):
        left, top = self.getScreenPosition(point)
        textSurface = self.font.render(symbol, True, BASE_COLOR["BLACK"])
        widthRatio = 0.55
        stretchedTextSurface = pygame.transform.smoothscale(
            textSurface,
            (math.ceil(self.blocksize_x * widthRatio), math.ceil(self.blocksize_y)),
        )
        textRect = stretchedTextSurface.get_rect(
            center=(left + self.blocksize_x / 2, top + self.blocksize_y / 2)
        )
        self.surface.blit(stretchedTextSurface, textRect)
