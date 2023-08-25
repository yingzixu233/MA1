from shapely.geometry import Polygon
import matplotlib.pyplot as plt

import module_extractor


class CorridorModule:
    # 默认走道模块为矩形

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
        print(f'Corridor Module {self.global_id} is deleted.')

    def show_corridor_module(self):
        plt.plot(*self.shape.exterior.xy, color='Yellow')

    @staticmethod
    def corridor_list_existing():
        corridor_list = []
        for i in range(0, len(CorridorModule.a.corridor_modules)):
            existing_corridor = CorridorModule(CorridorModule.a.get_corridor_id()[i],
                                               CorridorModule.a.get_corridor_coordinates()[i][0],
                                               CorridorModule.a.get_corridor_coordinates()[i][1],
                                               CorridorModule.a.get_corridor_dimensions()[i][0],
                                               CorridorModule.a.get_corridor_dimensions()[i][1])
            corridor_list.append(existing_corridor)
        return corridor_list

