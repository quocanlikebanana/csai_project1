from algorithm.astar import *
from algorithm.bfs import *
from component.enviroment import Enviroment
from component.moving import ConstantOrbit, LinearOrbit, RatioOrbit
from component.point import Point
from component.polygon import Polygon
from graphics.drawer import Drawer
from algorithm.dijkstra import *

def test2():
    pl = [
        Polygon(
            [Point(2, 2), Point(4, 2), Point(4, 4), Point(2, 4)]
        ),
        Polygon(
            [Point(12, 2), Point(14, 2), Point(14, 4), Point(12, 4)]
        ),
        Polygon(
            [Point(22, 2), Point(24, 2), Point(24, 4), Point(22, 4)]
        )
        ,
        Polygon(
            [Point(4, 10), Point(10, 20), Point(26, 20), Point(26, 10)]
        ),
        Polygon(
            [Point(2, 20), Point(8, 20), Point(8, 26), Point(2, 26)]
        )
    ]
    env = Enviroment(30, 30, Point(1, 1), Point(28, 28), [], pl)

    #BFS
    bfs = BFS(env)

    #Dijkstra
    dijkstra = Dijkstra(env)

    md = Drawer(env,dijkstra.searchOnce)
    md.runDraw()



test2()