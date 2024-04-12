from component.point import Point
from component.polygon import Polygon

#input = InputReader('input.txt')
#access to input. width, height, start_point, end_point, number_of_polygons, polygons
class MapReader:
    def __init__(self, file_path) -> None:
        f = open(file_path,'r')
        file_content  = f.read()
        lines = file_content.split('\n')

        #width and height of map
        tmp = lines[0].split(',')
        self.width = tmp[0]
        self.height = tmp[1]

        #start, end and meeting points
        tmp = lines[1].split(',')
        self.start_point = Point(tmp[0], tmp[1])
        self.end_point = Point(tmp[2], tmp[3])

        self.meeting_points :list[Point] = []
        k = 4
        while k<len(tmp):
            self.meeting_points.append(Point(tmp[k], tmp[k+1]))
            k = k+2
            
        #number of polygons
        self.number_of_polygons = int(lines[2])

        #vertex of polygons
        self.polygons :list[Polygon] = []
        for i in range(0, self.number_of_polygons):
            index = i+3
            tmp = lines[index].split(',')
            list_point : list[Point] = []
            j = 0
            while j<len(tmp):
                list_point.append(Point(tmp[j], tmp[j+1]))
                j = j+2
            self.polygons.append(Polygon(list_point))

    #for testing
    def output(self):
        print(self.width, self.height, '\n')
        print(self.start_point, self.end_point, '\n')
        print(self.number_of_polygons, '\n')
        for i in range(self.number_of_polygons):
            print(self.polygons[i], '\n')

