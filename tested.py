from algorithm.astar import *
from component.enviroment import Enviroment
from component.point import Point
from component.polygon import Polygon
from graphics.drawer import Drawer


def test2():
    pl = [
        Polygon(
            [
                Point(2, 4),
                Point(14, 1),
                Point(21, 17),
                Point(3, 21),
                Point(9, 13),
                Point(25, 7),
            ]
        ),
        Polygon([Point(2, 2), Point(4, 1), Point(7, 5)]),
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
    env = Enviroment(30, 25, Point(1, 1), Point(28, 23), [], pl)
    astar = AStar(AS_Map(env), EuclideanHeuristic)
    md = Drawer(env, astar.searchOnce)
    md.runDraw()


test2()  # env khong thoa
