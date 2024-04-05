from algorithm.astar import *
from component.enviroment import Enviroment
from component.point import Point, Velocity
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
        ),
    ]
    env = Enviroment(30, 25, Point(1, 1), Point(28, 23), [], pl)
    astar = AStar(AS_Map(env), EuclideanHeuristic)
    md = Drawer(env, astar.searchOnce)
    md.runDraw()


test2()
