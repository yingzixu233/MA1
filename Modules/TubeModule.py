from shapely.geometry import Polygon
import matplotlib.pyplot as plt

import module_extractor


# 创建模块类的意义在于可以建立新的类实例，以便对原图进行修改操作，所以不仅仅是存储原图信息，建立一个静态方法把信息导进类数组里
class TubeModule:
    # 默认核心筒模块为矩形

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
        print(f'Tube {self.global_id} is deleted.')

    def show_tube(self):
        plt.plot(*self.shape.exterior.xy, color='Red')

    @staticmethod
    def tube_list_existing():
        tube_list = []
        # 静态类变量的前缀是类
        for i in range(0, len(TubeModule.a.tube_modules)):
            existing_tube = TubeModule(TubeModule.a.get_tube_id()[i],
                                       TubeModule.a.get_tube_coordinates()[i][0],
                                       TubeModule.a.get_tube_coordinates()[i][1],
                                       TubeModule.a.get_tube_dimensions()[i][0],
                                       TubeModule.a.get_tube_dimensions()[i][1])
            tube_list.append(existing_tube)
        return tube_list

# 把每一个模块都写成类， 在图形数据库中对应节点，
# 基本模块和附属模块有对应的属性
# 类中存储形状，也存储信息
# 通过类可以创建数据库，可以创建插件（shapely）

# 怎么实现的自动，现有的ifc文件中提取信息，把它转化成类中的信息，形成一个一个类实例，再把他们生成平面图（matplotlib）
# 怎么实现的自动，现有的ifc文件中提取信息，把它转化成类中的信息，形成一个一个类实例，再把他们生成图形数据库
# 图形数据库可以修改平面图布局 修改后的映射回revit, 做成插件
