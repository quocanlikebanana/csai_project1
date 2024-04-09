from algorithm.astar import *
from algorithm.bfs import *
from algorithm.dijkstra import Dijkstra
from algorithm.ids import IDS
from algorithm.TSP import TSP
from component.enviroment import Enviroment
from component.moving import ConstantOrbit, LinearOrbit, RatioOrbit
from component.point import Point
from component.polygon import Polygon
from graphics.drawer import Drawer


class Main:
    def __init__(self, env, searchOnce=None) -> None:
        self.drawer = Drawer(env)
        self.drawer.graphics.runAlgorithmOnce = searchOnce
        pass

    def run(self):
        self.drawer.run()


def test():
    pl = [
        # Polygon([Point(2, 2), Point(4, 2), Point(4, 4), Point(2, 4)]),
        # Polygon([Point(12, 2), Point(14, 2), Point(14, 4), Point(12, 4)]),
        # Polygon([Point(22, 2), Point(24, 2), Point(24, 4), Point(22, 4)]),
        # Polygon([Point(4, 10), Point(10, 20), Point(26, 20), Point(26, 10)]),
        # Polygon(
        #     [Point(2, 20), Point(8, 20), Point(8, 26), Point(2, 26)],
        #     # LinearOrbit([Point(0, 0), Point(2, 2)], 10),
        # ),
    ]
    env = Enviroment(30, 30, Point(1, 1), Point(28, 28), [Point(10,20),Point(2,10),Point(8,5),Point(20,5)], pl)

    # BFS
    bfs = BFS(env)
    astar = AStar(AS_Map(env), EuclideanHeuristic)
    ids = IDS(env)
    dij = Dijkstra(env)
    tsp = TSP(env,EuclideanHeuristic)
    main = Main(env, tsp.searchOnce)
    main.run()


if __name__ == "__main__":
    import cProfile, pstats
    from pstats import SortKey
    import io

    s = io.StringIO()
    cProfile.run("test()", "test_stats")
    ps = pstats.Stats("test_stats", stream=s)
    ps.sort_stats(SortKey.TIME).print_stats(0.20)


    with open("test.txt", "w+") as f:
        f.write(s.getvalue())

    # profiler = cProfile.Profile()
    # profiler.enable()
    # test()
    # profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats("ncalls")
    # stats.print_stats()
