import matplotlib.pyplot as plt

from Modules import BasicModule
from Modules import ConjunctiveModule


class HousePlan:

    def __init__(self,
                 basic_modules: list[BasicModule],
                 conjunctive_modules: list[ConjunctiveModule],
                 ):
        self.basic_modules = basic_modules
        self.conjunctive_modules = conjunctive_modules

    def __del__(self):
        print(f'The house plan is deleted.')

    def show_housePlan(self):
        if not self.basic_modules:
            print("Basic modules are missing. The house plan is not feasible!")
            del self
        else:
            for basic_module in self.basic_modules:
                plt.plot(*basic_module.shape.exterior.xy, color='DarkBlue')
            for conjunctive_module in self.conjunctive_modules:
                plt.plot(*conjunctive_module.shape.exterior.xy, color='LightBlue')

    @staticmethod
    def house_list_existing():
        house_list = []

        return house_list


        # 怎么确认输入参数就是基本模块和拼接模块数组
        # 不同的户型不需要标号的吗
        # 相同户型怎么匹配，怎么进行相似度分析（连接关系和模块尺寸是完全相同的）
        # 是不是要在户型里定义某种强连接的关系，还是在neo4j里面设置，应该是在revit里抓取的信息导入到python里面，然后把信息再还原到NEO4J里
        # 如果基本模块不存在，那么户型就不成立


