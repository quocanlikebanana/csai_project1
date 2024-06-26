from component.moving import VeloOrbit
from component.point import Point
from component.polygon import Polygon
from component.environment import Environment


# input = InputReader('input.txt')
# access to input. width, height, start_point, end_point, number_of_polygons, polygons, meetings_point
class MapReader:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.width = 0
        self.height = 0
        self.start_point: Point = None
        self.end_point: Point = None
        self.number_of_polygons = 0
        self.polygons: list[Polygon] = []
        self.meeting_points: list[Point] = []

    def create_environment(self):
        f = open(self.file_path, "r")
        file_content = f.read()
        lines = file_content.split("\n")

        # width and height of map
        tmp = lines[0].split(",")
        self.width = int(tmp[0])
        self.height = int(tmp[1])

        # start, end and meeting points
        tmp = lines[1].split(",")
        self.start_point = Point(tmp[0], tmp[1])
        self.end_point = Point(tmp[2], tmp[3])

        k = 4
        while k < len(tmp):
            self.meeting_points.append(Point(tmp[k], tmp[k + 1]))
            k = k + 2

        # number of polygons
        self.number_of_polygons = int(lines[2])

        # vertex of polygons
        self.polygons: list[Polygon] = []
        for i in range(0, self.number_of_polygons):
            orbit = None
            index = i + 3
            poly = lines[index].split("|")
            if len(poly) > 1:
                tmpvec = poly[1].split(",")
                k = 0
                list_vec = []
                while k < len(tmpvec):
                    list_vec.append(
                        (float(tmpvec[k]), float(tmpvec[k + 1]), float(tmpvec[k + 2]))
                    )
                    k += 3
                orbit = VeloOrbit(list_vec)
            tmp = poly[0].split(",")
            list_point: list[Point] = []
            j = 0
            while j < len(tmp):
                list_point.append(Point(tmp[j], tmp[j + 1]))
                j = j + 2
            self.polygons.append(Polygon(list_point, orbit))
        pass

        E = Environment(
            self.width + 1,
            self.height + 1,
            self.start_point,
            self.end_point,
            self.meeting_points,
            self.polygons,
        )
        return E

    # for testing
    def output(self):
        print(self.width, self.height, "\n")
        print(self.start_point, self.end_point, "\n")
        print(self.number_of_polygons, "\n")
        for i in range(self.number_of_polygons):
            print(self.polygons[i], "\n")
