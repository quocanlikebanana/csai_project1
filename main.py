from algorithm.astar import *
from algorithm.bfs import *
from algorithm.dijkstra import Dijkstra
from algorithm.dfs import DFS
from algorithm.dstar import DStar
from component.environment import Environment
from component.moving import VeloOrbit
from component.point import Point
from component.polygon import Polygon
from graphics.drawer import Drawer
from input.input import InputReader


class Main:
    def __init__(self, env, searchOnce=None) -> None:
        self.drawer = Drawer(env)
        self.drawer.graphics.runAlgorithmOnce = searchOnce
        pass

    def run(self):
        self.drawer.run()


def test():
    env = Enviroment(
        30,
        30,
        Point(1, 1),
        Point(28, 28),
        [],
        [
            Polygon(
                [Point(2, 2), Point(4, 2), Point(4, 4), Point(2, 4)],
                VeloOrbit([(-1, 0, 1), (1, 0, 1)]),
            ),
            Polygon([Point(12, 2), Point(14, 2), Point(14, 4), Point(12, 4)]),
            Polygon([Point(22, 2), Point(24, 2), Point(24, 4), Point(22, 4)]),
            Polygon(
                [Point(4, 10), Point(10, 20), Point(26, 20), Point(26, 10)],
                VeloOrbit([(-1, 2, 2), (1, -2, 2)]),
            ),
            Polygon(
                [Point(2, 20), Point(8, 20), Point(8, 26), Point(2, 26)],
                VeloOrbit([(1, 1, 1), (-1, -1, 1)]),
            ),
        ],
    )

    # bfs = BFS(env)
    # astar = AStar(AS_Map(env), EuclideanHeuristic)
    # dfs = DFS(env)
    # dij = Dijkstra(env)
    dstar = DStar(env)
    # main = Main(env, dfs.searchOnce)

    main = Main(env, dstar.searchOnce)

    # main = Main(env)
    main.run()


def test2():
    env = Enviroment(
        30,
        20,
        Point(3, 2),
        Point(26, 15),
        [],
        [
            Polygon(
                [Point(12, 10), Point(14, 10), Point(14, 17), Point(12, 17)],
                VeloOrbit([(0, -1, 3), (0, 1, 3)]),
            ),
            Polygon(
                [Point(5, 1), Point(8, 1), Point(5, 10)],
                VeloOrbit([(0, 1, 2), (0, -1, 2)]),
            ),
        ],
    )
    main = Main(env, DStar(env).searchOnce)
    main.run()


def test3():
    env = Enviroment(
        30,
        20,
        Point(3, 2),
        Point(26, 10),
        [],
        [
            Polygon(
                [Point(12, 1), Point(14, 1), Point(14, 17), Point(12, 17)],
                VeloOrbit([(0, 1, 1), (0, -1, 1)]),
            ),
        ],
    )
    main = Main(env, DStar(env).searchOnce)
    main.run()


def test4():
    env = Enviroment(
        30,
        20,
        Point(1, 18),
        Point(28, 18),
        [],
        [
            Polygon(
                [Point(7, 3), Point(7, 16), Point(8, 16), Point(8, 3)],
                VeloOrbit([(0, -1, 2), (0, 1, 2)]),
            ),
            Polygon([Point(9, 15), Point(9, 18), Point(10, 18), Point(10, 15)]),
        ],
    )
    main = Main(env, DStar(env).searchOnce)
    main.run()


def test5():
    env = Enviroment(
        30,
        20,
        Point(1, 18),
        Point(28, 18),
        [],
        [
            Polygon(
                [Point(10, 8), Point(10, 16), Point(11, 16), Point(11, 8)],
                VeloOrbit(
                    [
                        (0, -1, 4),
                        (0, 1, 5),
                        (0, -1, 1),
                    ]
                ),
            ),
            Polygon([Point(12, 13), Point(12, 18), Point(13, 18), Point(13, 13)]),
            Polygon([Point(12, 1), Point(12, 8), Point(13, 8), Point(13, 1)]),
        ],
    )
    main = Main(env, DStar(env).searchOnce)
    main.run()


if __name__ == "__main__":
    import cProfile, pstats
    from pstats import SortKey
    import io

    s = io.StringIO()
    cProfile.run("test5()", "test_stats")
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
