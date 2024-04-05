import pygame
import sys
import math
import os

from component.enviroment import Enviroment
from component.point import Point
from graphics.color import BASE_COLOR

MAX_FPS = 1000


class Graphics:
    def __init__(self, env: Enviroment, runinitdraw, runAlgorithmOnce) -> None:
        self.env = env
        self.MAR_X = 0
        self.MAR_Y = 0
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
        self.runinitdraw = runinitdraw
        self.runAlgorithmOnce = runAlgorithmOnce

    def updateBlockSize(self):
        windowWidth, windowHeight = pygame.display.get_surface().get_size()
        self.blocksize_x = (windowWidth - self.MAR_X * 2) / self.env.ncol
        self.blocksize_y = (windowHeight - self.MAR_Y * 2) / self.env.nrow

    def getScreenPosition(self, point: Point):
        left = self.MAR_X + self.blocksize_x * point.x
        top = self.MAR_Y + self.blocksize_y * point.y
        return left, top

    def runRender(self) -> None:
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
        self.updateBlockSize()
        self.clock.tick(MAX_FPS)

        # Loop
        while True:
            self.surface.fill(BASE_COLOR["WHITE"])
            self.runinitdraw()
            self.runAlgorithmOnce()
            pygame.display.update()
            # Event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.updateBlockSize()

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
        stretchedTextSurface = pygame.transform.smoothscale(
            textSurface,
            (math.ceil(self.blocksize_x * 0.55), math.ceil(self.blocksize_y)),
        )
        textRect = stretchedTextSurface.get_rect(
            center=(left + self.blocksize_x / 2, top + self.blocksize_y / 2)
        )
        self.surface.blit(stretchedTextSurface, textRect)
