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


class Main:
    def __init__(self, env, searchOnce=None) -> None:
        self.drawer = Drawer(env)
        self.drawer.graphics.runAlgorithmOnce = searchOnce
        pass

    def run(self):
        self.drawer.run()


def test():
    pl = [
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
    ]
    env = Environment(30, 30, Point(1, 1), Point(28, 28), [], pl)

    # bfs = BFS(env)
    # astar = AStar(AS_Map(env), EuclideanHeuristic)
    # dfs = DFS(env)
    # dij = Dijkstra(env)
    dstar = DStar(env)
    # main = Main(env, dfs.searchOnce)

    main = Main(env, dstar.searchOnce)

    # main = Main(env)

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
