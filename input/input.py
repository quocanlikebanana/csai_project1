import os.path

from algorithm.TSP import TSP
from algorithm.bfs import BFS
from algorithm.dfs import DFS
from algorithm.astar import AS_Map, AStar
from algorithm.dijkstra import Dijkstra
from algorithm.dstar import DStar
from main import Main
from map_reader.map_reader import MapReader
from enum import Enum


class ALGORITHM_NAME(Enum):
    BFS: 1
    DFS: 2
    DIJKSTRA: 3
    ASTAR: 4
    TSP: 5
    DSTAR: 6


def create_algorithm(env, level, algorithm):
    if level == 1:
        return BFS(env)
    if level == 3:
        return TSP(env)
    if level == 4:
        return DStar(env)

    if algorithm == 1:
        return DFS(env)
    if algorithm == 2:
        return Dijkstra(env)
    if algorithm == 3:
        return AStar(AS_Map(env))


class Input:
    def __init__(self) -> None:
        self.level = 0
        self.file_path = ""
        self.algorithm = 0  # neu la muc 2 thi moi co thuat toan

    def is_level(self, input):
        return int(input) in range(1, 5)

    def is_file_exist(self, input):
        return os.path.isfile(input)

    def run(self):
        print(
            """\n*Lưu ý:
              Nhập "b" (back) để quay về lựa chọn trước đó
              Nhập "s" (stop) để dừng chương trình\n"""
        )
        while True:
            while not self.is_level(self.level):
                self.level = input(
                    """1)Lựa chọn mức độ thực hiện [1,2,3,4,b,s]
                VD: nhập "1" để chọn mức độ 1
                Giá trị nhận vào: """
                )
                if self.level in ["b", "s"]:
                    return
                elif not self.is_level(self.level):
                    print("Thông báo: Giá trị không hợp lệ, vui lòng chọn lại\n")
                else:
                    self.level = int(self.level)
                    while not self.is_file_exist(self.file_path):
                        self.file_path = input(
                            """2)Nhập tên file [file_name,b,s]
                VD: nhập "input.txt" để chọn file input.txt
                Giá trị nhận vào: """
                        )

                        if self.file_path == "b":
                            break
                        elif self.file_path == "s":
                            return
                        elif not self.is_file_exist("./input_files/" + self.file_path):
                            print("Thông báo: Không tìm thấy file, vui lòng chọn lại\n")
                        else:
                            self.file_path = "./input_files/" + self.file_path
                            if int(self.level) == 2:
                                while not int(self.algorithm) in range(1, 4):
                                    self.algorithm = input(
                                        """3)Chọn thuật toán cho mức 2 [1,2,3,b,s]
                            Nhập "1" để chọn DFS
                            Nhập "2" để chọn Dijkstra
                            Nhập "3" để chọn Astar
                            Giá trị nhận vào: """
                                    )
                                    if self.algorithm == "b":
                                        self.algorithm = 0
                                        break
                                    elif self.algorithm == "s":
                                        self.algorithm = 0
                                        return
                                    elif not int(self.algorithm) in range(1, 4):
                                        print(
                                            "Thông báo: Giá trị không hợp lệ, vui lòng chọn lại\n"
                                        )
                                    else:
                                        # print(
                                        #     "gọi lệnh chạy mức 2 với thuật toán được chọn\n"
                                        # )
                                        env = MapReader(
                                            self.file_path
                                        ).create_environment()
                                        self.algorithm = int(self.algorithm)
                                        try:
                                            run_algorithm = create_algorithm(
                                                env, self.level, self.algorithm
                                            )
                                            Main(env, run_algorithm.searchOnce).run()
                                        except ValueError as e:
                                            print(str(e))
                                        self.algorithm = 0
                            else:
                                # print("gọi lệnh chạy mức 1,3,4\n")
                                env = MapReader(self.file_path).create_environment()
                                try:
                                    run_algorithm = create_algorithm(
                                        env, self.level, self.algorithm
                                    )
                                    Main(env, run_algorithm.searchOnce).run()
                                except ValueError as e:
                                    print(str(e))

                        self.file_path = ""

                self.level = 0


Input().run()
