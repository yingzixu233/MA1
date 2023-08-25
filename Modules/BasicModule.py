from shapely.geometry import Polygon
import matplotlib.pyplot as plt

import module_extractor


class BasicModule:
    # 默认基本模块为矩形

    # 静态变量，是模块抽取器的类实例，它包括从IFC文件中获得的所有信息
    a = module_extractor.ModuleExtractor('MA-Case Study.ifc')

    def __init__(self, global_id, x_coordinate, y_coordinate, width, height):
        self.global_id = global_id
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height
        self.shape = Polygon([(x_coordinate - width / 2, y_coordinate - height / 2),
                              (x_coordinate - width / 2, y_coordinate + height / 2),
                              (x_coordinate + width / 2, y_coordinate + height / 2),
                              (x_coordinate + width / 2, y_coordinate - height / 2)])

    def __del__(self):
        print(f'Basic Module {self.global_id} is deleted.')

    def show_basic_module(self):
        plt.plot(*self.shape.exterior.xy, color='DarkBlue')

    @staticmethod
    def basic_list_existing():
        basic_list = []
        for i in range(0, len(BasicModule.a.basic_modules)):
            existing_basic = BasicModule(BasicModule.a.get_basic_id()[i],
                                         BasicModule.a.get_basic_coordinates()[i][0],
                                         BasicModule.a.get_basic_coordinates()[i][1],
                                         BasicModule.a.get_basic_dimensions()[i][0],
                                         BasicModule.a.get_basic_dimensions()[i][1])
            basic_list.append(existing_basic)
        return basic_list

