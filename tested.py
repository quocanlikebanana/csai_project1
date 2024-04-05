from algorithm.astar import *
from component.enviroment import Enviroment
from component.moving import LinearOrbit, ConstantOrbit
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
            ],
            ConstantOrbit(0.5, 0),
        ),
    ]
    env = Enviroment(30, 25, Point(1, 1), Point(28, 23), [], pl)
    astar = AStar(AS_Map(env), EuclideanHeuristic)
    md = Drawer(env, astar.searchOnce)
    md.runDraw()


test2()


def test1():
    pl = [
        Polygon([Point(2, 2), Point(4, 1), Point(7, 5)]),
        Polygon([Point(19, 5), Point(34, 15), Point(42, 52), Point(12, 42)]),
        Polygon([Point(9, 1), Point(18, 5), Point(5, 19)]),
    ]
    env = Enviroment(45, 55, Point(1, 1), Point(43, 35), [], pl)
    astar = AStar(AS_Map(env), EuclideanHeuristic)
    md = Drawer(env, astar.searchOnce)
    md.runDraw()


test1()


def test3():
    pl = [
        Polygon(
            [
                Point(2, 4),
                Point(14, 2),
                Point(21, 17),
                Point(3, 21),
                Point(5, 13),
                Point(25, 7),
            ],
            LinearOrbit([Point(1, 2), Point(1, 7), Point(4, 2)], 10),
        ),
        Polygon(
            [Point(1, 10), Point(1, 8), Point(6, 8)],
            ConstantOrbit([Point(3, 4), Point(3, 5)], 5),
        ),
    ]
    env = Enviroment(30, 25, Point(1, 1), Point(28, 23), [], pl)
    md = Drawer(env)
    md.runDraw()


test3()
