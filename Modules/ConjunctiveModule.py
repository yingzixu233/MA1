from shapely.geometry import Polygon
import matplotlib.pyplot as plt

import module_extractor


class ConjunctiveModule:
    # 默认拼接模块为矩形

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
        print(f'Conjunctive Module {self.global_id} is deleted.')

    def show_conjunctive_module(self):
        plt.plot(*self.shape.exterior.xy, color='LightBlue')

    @staticmethod
    def conjunct_list_existing():
        conjunct_list = []
        for i in range(0, len(ConjunctiveModule.a.conjunctive_modules)):
            existing_conjunct = ConjunctiveModule(ConjunctiveModule.a.get_conjunct_id()[i],
                                                  ConjunctiveModule.a.get_conjunct_coordinates()[i][0],
                                                  ConjunctiveModule.a.get_conjunct_coordinates()[i][1],
                                                  ConjunctiveModule.a.get_conjunct_dimensions()[i][0],
                                                  ConjunctiveModule.a.get_conjunct_dimensions()[i][1])
            conjunct_list.append(existing_conjunct)
        return conjunct_list
