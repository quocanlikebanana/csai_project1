import os.path

class Input:
    def __init__(self) -> None:
        self.level = 0
        self.file_path = ""
        self.algorithm = 0 # neu la muc 2 thi moi co thuat toan
 
    def  is_level(self, input):
        return int(input) in range(1,5)
    
    def is_file_exist(self, input):
        return os.path.isfile(f'./input_files/{input}')
    
    def run(self):
        print('''\n*Lưu ý:
              Nhập "b" (back) để quay về lựa chọn trước đó
              Nhập "s" (stop) để dừng chương trình\n''')
        while True:
            while not self.is_level(self.level):
                self.level = input('''1)Lựa chọn mức độ thực hiện [1,2,3,4,b,s]
                VD: nhập "1" để chọn mức độ 1
                Giá trị nhận vào: ''')
                if self.level in ['b','s']:
                    return
                elif not self.is_level(self.level):
                    print('Thông báo: Giá trị không hợp lệ, vui lòng chọn lại\n')
                else:
                    while not self.is_file_exist(self.file_path):
                        self.file_path = input('''2)Nhập tên file [file_name,b,s]
                VD: nhập "input.txt" để chọn file input.txt
                Giá trị nhận vào: ''')    

                        if self.file_path =='b':
                            break
                        elif self.file_path =='s':
                            return
                        elif not self.is_file_exist(self.file_path):
                            print('Thông báo: Không tìm thấy file, vui lòng chọn lại\n')
                        elif int(self.level) == 2:
                            while not int(self.algorithm) in range(1,4):
                                self.algorithm = input('''3)Chọn thuật toán cho mức 2 [1,2,3,b,s]
                        Vd: 
                        nhập "1" để chọn BFS
                        nhập "2" để chọn DFS
                        nhập "3" để chọn Dijkstra
                        Giá trị nhận vào: ''')  
                                if self.algorithm =='b':
                                    break
                                elif self.algorithm =='s':
                                    return
                                elif not int(self.algorithm) in range(1,4):
                                    print('Thông báo: Giá trị không hợp lệ, vui lòng chọn lại\n') 
                                else:
                                    print('gọi lệnh chạy mức 2 với thuật toán được chọn\n')   
                                    self.algorithm = 0  
                        else:
                            print('gọi lệnh chạy mức 1,3,4\n')   
                            self.file_path = ""  

                    self.level = 0     


    
Input().run()