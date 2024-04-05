from algorithm.astar import *
from component.enviroment import Enviroment
from component.point import Point
from component.polygon import Polygon
from graphics.drawer import EnvDrawer


def test1():
    pl = [
        Polygon([Point(2, 2), Point(4, 1), Point(7, 5)]),
        Polygon([Point(19, 5), Point(34, 15), Point(42, 52), Point(12, 42)]),
        Polygon([Point(9, 1), Point(18, 5), Point(5, 19)]),
        Polygon([Point(24, 16), Point(24, 19), Point(27, 19), Point(27, 16)]),
        Polygon(
            [
                Point(16, 2),
                Point(23, 2),
                Point(23, 10),
                Point(20, 10),
                Point(20, 5),
                Point(16, 5),
            ]
        ),
    ]
    env = Enviroment(45, 55, Point(1, 1), Point(43, 53), [], pl)
    astar = AStar(AS_Map(env), EuclideanHeuristic)
    md = EnvDrawer(env, astar.searchOnce)
    md.runInitDraw()


test1()  # Co van de voi viec di cheo
