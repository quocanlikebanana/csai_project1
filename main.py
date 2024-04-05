from algorithm.astar import *
from component.enviroment import Enviroment
from component.moving import ConstantOrbit, LinearOrbit, RatioOrbit
from component.point import Point
from component.polygon import Polygon
from graphics.drawer import Drawer


def test2():
    pl = [
        Polygon(
            [Point(2, 2), Point(4, 2), Point(4, 4), Point(2, 4)],
            ConstantOrbit(
                [Point(0, 0), Point(0, 4), Point(2, 4), Point(5, 4), Point(5, 14)], 50
            ),
        ),
        Polygon(
            [Point(12, 2), Point(14, 2), Point(14, 4), Point(12, 4)],
            LinearOrbit([Point(0, 0), Point(0, 4), Point(2, 17)], 15),
        ),
        Polygon(
            [Point(22, 2), Point(24, 2), Point(24, 4), Point(22, 4)],
            RatioOrbit([Point(0, 0), Point(5, 4), Point(2, 22), Point(-12, 4)], 0.5),
        ),
    ]
    env = Enviroment(30, 30, Point(1, 1), Point(28, 28), [], pl)
    md = Drawer(env)
    md.runDraw()


test2()
