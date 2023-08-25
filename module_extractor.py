import ifcopenshell


class ModuleExtractor:

    def __init__(self, path):
        self.storey = ifcopenshell.open(path).by_type("IfcBuildingStorey")
        self.house_level = list(filter(lambda l: l.Name == "House Plan", self.storey))
        self.module_level = list(filter(lambda l: l.Name == "Module", self.storey))
        self.modules = ifcopenshell.open(path).by_type("IfcBuildingElementProxy")
        self.tube_modules = list(filter(lambda t: t.ObjectType == 'Modules:Tube module', self.modules))
        self.corridor_modules = list(filter(lambda c: 'Modules:Corridor module' in c.ObjectType, self.modules))
        self.basic_modules = list(filter(lambda b: b.ObjectType == 'Modules:Basic module', self.modules))
        self.conjunctive_modules = list(filter(lambda c: c.ObjectType == 'Modules:Conjunctive module', self.modules))
        self.walls = ifcopenshell.open(path).by_type("IfcWallStandardCase")

    def get_tube_id(self):
        tube_id = []
        for tube in self.tube_modules:
            tube_id.append(tube.GlobalId)
        return tube_id

    def get_basic_id(self):
        basic_id = []
        for basic in self.basic_modules:
            basic_id.append(basic.GlobalId)
        return basic_id

    def get_corridor_id(self):
        corridor_id = []
        for corridor in self.corridor_modules:
            corridor_id.append(corridor.GlobalId)
        return corridor_id

    def get_conjunct_id(self):
        conjunct_id = []
        for conjunct in self.conjunctive_modules:
            conjunct_id.append(conjunct.GlobalId)
        return conjunct_id

    def get_tube_coordinates(self):
        tube_coordinates = []
        for tube in self.tube_modules:
            (x, y) = (tube.ObjectPlacement.RelativePlacement.Location.Coordinates[0],
                      tube.ObjectPlacement.RelativePlacement.Location.Coordinates[1])
            tube_coordinates.append((round(x), round(y)))
        return tube_coordinates

    def get_basic_coordinates(self):
        basic_coordinates = []
        for basic in self.basic_modules:
            (x, y) = (basic.ObjectPlacement.RelativePlacement.Location.Coordinates[0],
                      basic.ObjectPlacement.RelativePlacement.Location.Coordinates[1])
            basic_coordinates.append((round(x), round(y)))
        return basic_coordinates

    def get_corridor_coordinates(self):
        corridor_coordinates = []
        for corridor in self.corridor_modules:
            (x, y) = (corridor.ObjectPlacement.RelativePlacement.Location.Coordinates[0],
                      corridor.ObjectPlacement.RelativePlacement.Location.Coordinates[1])
            corridor_coordinates.append((round(x), round(y)))
        return corridor_coordinates

    def get_conjunct_coordinates(self):
        conjunct_coordinates = []
        for conjunct in self.conjunctive_modules:
            (x, y) = (conjunct.ObjectPlacement.RelativePlacement.Location.Coordinates[0],
                      conjunct.ObjectPlacement.RelativePlacement.Location.Coordinates[1])
            conjunct_coordinates.append((round(x), round(y)))
        return conjunct_coordinates

    def get_tube_dimensions(self):
        tube_dimensions = []
        for tube in self.tube_modules:
            (width, height, depth) = (
                tube.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue,
                tube.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue,
                tube.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[2].NominalValue.wrappedValue)
            tube_dimensions.append((round(width), round(height), round(depth)))
        return tube_dimensions

    def get_basic_dimensions(self):
        basic_dimensions = []
        for basic in self.basic_modules:
            (width, height, depth) = (
                basic.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue,
                basic.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue,
                basic.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[2].NominalValue.wrappedValue)
            basic_dimensions.append((round(width), round(height), round(depth)))
        return basic_dimensions

    def get_corridor_dimensions(self):
        corridor_dimensions = []
        for corridor in self.corridor_modules:
            (width, height, depth) = (
                corridor.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue,
                corridor.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue,
                corridor.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[2].NominalValue.wrappedValue)
            corridor_dimensions.append((round(width), round(height), round(depth)))
        return corridor_dimensions

    def get_conjunct_dimensions(self):
        conjunct_dimensions = []
        for conjunct in self.conjunctive_modules:
            (width, height, depth) = (
                conjunct.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue,
                conjunct.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue,
                conjunct.IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[2].NominalValue.wrappedValue)
            conjunct_dimensions.append((round(width), round(height), round(depth)))
        return conjunct_dimensions

    # 获取模块之间的邻接关系，是否邻接，上下邻接还是左右邻接, 谁在上下，谁在左右
    def get_tube_basic_adjacency(self):
        adjacency = []
        n = len(self.get_tube_id())
        m = len(self.get_basic_id())
        tube_coordinates = self.get_tube_coordinates()
        basic_coordinates = self.get_basic_coordinates()
        tube_dimensions = self.get_tube_dimensions()
        basic_dimensions = self.get_basic_dimensions()
        eps = 1e-4
        for i in range(0, n):
            for j in range(0, m):
                x_diff = tube_coordinates[i][0] - basic_coordinates[j][0]
                a = abs(x_diff) - 0.5 * (tube_dimensions[i][0] + basic_dimensions[j][0])
                y_diff = tube_coordinates[i][1] - basic_coordinates[j][1]
                b = abs(y_diff) - 0.5 * (tube_dimensions[i][1] + basic_dimensions[j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([tube_coordinates[i][1] - 0.5 * tube_dimensions[i][1],
                                        tube_coordinates[i][1] + 0.5 * tube_dimensions[i][1],
                                        basic_coordinates[i][1] + 0.5 * basic_dimensions[i][1],
                                        basic_coordinates[i][1] - 0.5 * basic_dimensions[i][1]])
                    if x_diff > 0:
                        co_edge_x = tube_coordinates[i][0] - 0.5 * tube_dimensions[i][0]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = tube_coordinates[i][0] + 0.5 * tube_dimensions[i][0]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([tube_coordinates[i][0] - 0.5 * tube_dimensions[i][0],
                                        tube_coordinates[i][0] + 0.5 * tube_dimensions[i][0],
                                        basic_coordinates[i][0] + 0.5 * basic_dimensions[i][0],
                                        basic_coordinates[i][0] - 0.5 * basic_dimensions[i][0]])
                    if y_diff > 0:
                        co_edge_y = tube_coordinates[i][1] - 0.5 * tube_dimensions[i][1]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = tube_coordinates[i][1] + 0.5 * tube_dimensions[i][1]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_tube_id()[i],
                                      self.get_basic_id()[j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_tube_conjunct_adjacency(self):
        adjacency = []
        n = len(self.get_tube_id())
        m = len(self.get_conjunct_id())
        tube_coordinates = self.get_tube_coordinates()
        conjunct_coordinates = self.get_conjunct_coordinates()
        tube_dimensions = self.get_tube_dimensions()
        conjunct_dimensions = self.get_conjunct_dimensions()
        eps = 1e-4
        for i in range(0, n):
            for j in range(0, m):
                x_diff = tube_coordinates[i][0] - conjunct_coordinates[j][0]
                a = abs(x_diff) - 0.5 * (tube_dimensions[i][0] + conjunct_dimensions[j][0])
                y_diff = tube_coordinates[i][1] - conjunct_coordinates[j][1]
                b = abs(y_diff) - 0.5 * (tube_dimensions[i][1] + conjunct_dimensions[j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([tube_coordinates[i][1] - 0.5 * tube_dimensions[i][1],
                                        tube_coordinates[i][1] + 0.5 * tube_dimensions[i][1],
                                        conjunct_coordinates[i][1] + 0.5 * conjunct_dimensions[i][1],
                                        conjunct_coordinates[i][1] - 0.5 * conjunct_dimensions[i][1]])
                    if x_diff > 0:
                        co_edge_x = tube_coordinates[i][0] - 0.5 * tube_dimensions[i][0]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = tube_coordinates[i][0] + 0.5 * tube_dimensions[i][0]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([tube_coordinates[i][0] - 0.5 * tube_dimensions[i][0],
                                        tube_coordinates[i][0] + 0.5 * tube_dimensions[i][0],
                                        conjunct_coordinates[i][0] + 0.5 * conjunct_dimensions[i][0],
                                        conjunct_coordinates[i][0] - 0.5 * conjunct_dimensions[i][0]])
                    if y_diff > 0:
                        co_edge_y = tube_coordinates[i][1] - 0.5 * tube_dimensions[i][1]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = tube_coordinates[i][1] + 0.5 * tube_dimensions[i][1]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_tube_id()[i],
                                      self.get_conjunct_id()[j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_tube_corridor_adjacency(self):
        adjacency = []
        n = len(self.get_tube_id())
        m = len(self.get_corridor_id())
        tube_coordinates = self.get_tube_coordinates()
        corridor_coordinates = self.get_corridor_coordinates()
        tube_dimensions = self.get_tube_dimensions()
        corridor_dimensions = self.get_corridor_dimensions()
        eps = 1e-4
        for i in range(0, n):
            for j in range(0, m):
                x_diff = tube_coordinates[i][0] - corridor_coordinates[j][0]
                a = abs(x_diff) - 0.5 * (tube_dimensions[i][0] + corridor_dimensions[j][0])
                y_diff = tube_coordinates[i][1] - corridor_coordinates[j][1]
                b = abs(y_diff) - 0.5 * (tube_dimensions[i][1] + corridor_dimensions[j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([tube_coordinates[i][1] - 0.5 * tube_dimensions[i][1],
                                        tube_coordinates[i][1] + 0.5 * tube_dimensions[i][1],
                                        corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1],
                                        corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1]])
                    if x_diff > 0:
                        co_edge_x = tube_coordinates[i][0] - 0.5 * tube_dimensions[i][0]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_corridor_id()[j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = tube_coordinates[i][0] + 0.5 * tube_dimensions[i][0]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_corridor_id()[j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([tube_coordinates[i][0] - 0.5 * tube_dimensions[i][0],
                                        tube_coordinates[i][0] + 0.5 * tube_dimensions[i][0],
                                        corridor_coordinates[i][0] + 0.5 * corridor_dimensions[i][0],
                                        corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0]])
                    if y_diff > 0:
                        co_edge_y = tube_coordinates[i][1] - 0.5 * tube_dimensions[i][1]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_corridor_id()[j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = tube_coordinates[i][1] + 0.5 * tube_dimensions[i][1]
                        adjacency.append([self.get_tube_id()[i],
                                          self.get_corridor_id()[j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_tube_id()[i],
                                      self.get_corridor_id()[j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_basic_conjunct_adjacency(self):
        adjacency = []
        n = len(self.get_basic_id())
        m = len(self.get_conjunct_id())
        basic_coordinates = self.get_basic_coordinates()
        conjunct_coordinates = self.get_conjunct_coordinates()
        basic_dimensions = self.get_basic_dimensions()
        conjunct_dimensions = self.get_conjunct_dimensions()
        eps = 1e-4
        for i in range(0, n):
            for j in range(0, m):
                x_diff = basic_coordinates[i][0] - conjunct_coordinates[j][0]
                a = abs(x_diff) - 0.5 * (basic_dimensions[i][0] + conjunct_dimensions[j][0])
                y_diff = basic_coordinates[i][1] - conjunct_coordinates[j][1]
                b = abs(y_diff) - 0.5 * (basic_dimensions[i][1] + conjunct_dimensions[j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([basic_coordinates[i][1] + 0.5 * basic_dimensions[i][1],
                                        basic_coordinates[i][1] - 0.5 * basic_dimensions[i][1],
                                        conjunct_coordinates[j][1] + 0.5 * conjunct_dimensions[j][1],
                                        conjunct_coordinates[j][1] - 0.5 * conjunct_dimensions[j][1]])
                    if x_diff > 0:
                        co_edge_x = basic_coordinates[i][0] - 0.5 * basic_dimensions[i][0]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = basic_coordinates[i][0] + 0.5 * basic_dimensions[i][0]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([basic_coordinates[i][0] - 0.5 * basic_dimensions[i][0],
                                        basic_coordinates[i][0] + 0.5 * basic_dimensions[i][0],
                                        conjunct_coordinates[j][0] + 0.5 * conjunct_dimensions[j][0],
                                        conjunct_coordinates[j][0] - 0.5 * conjunct_dimensions[j][0]])
                    if y_diff > 0:
                        co_edge_y = basic_coordinates[i][1] - 0.5 * basic_dimensions[i][1]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = basic_coordinates[i][1] + 0.5 * basic_dimensions[i][1]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_basic_id()[i],
                                      self.get_conjunct_id()[j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_corridor_basic_adjacency(self):
        adjacency = []
        n = len(self.get_corridor_id())
        m = len(self.get_basic_id())
        corridor_coordinates = self.get_corridor_coordinates()
        basic_coordinates = self.get_basic_coordinates()
        corridor_dimensions = self.get_corridor_dimensions()
        basic_dimensions = self.get_basic_dimensions()
        eps = 1e-4
        for i in range(0, n):
            for j in range(0, m):
                x_diff = corridor_coordinates[i][0] - basic_coordinates[j][0]
                a = abs(x_diff) - 0.5 * (corridor_dimensions[i][0] + basic_dimensions[j][0])
                y_diff = corridor_coordinates[i][1] - basic_coordinates[j][1]
                b = abs(y_diff) - 0.5 * (corridor_dimensions[i][1] + basic_dimensions[j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1],
                                        corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1],
                                        basic_coordinates[j][1] + 0.5 * basic_dimensions[j][1],
                                        basic_coordinates[j][1] - 0.5 * basic_dimensions[j][1]])
                    if x_diff > 0:
                        co_edge_x = corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = corridor_coordinates[i][0] + 0.5 * corridor_dimensions[i][0]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0],
                                        corridor_coordinates[i][0] + 0.5 * corridor_dimensions[i][0],
                                        basic_coordinates[j][0] + 0.5 * basic_dimensions[j][0],
                                        basic_coordinates[j][0] - 0.5 * basic_dimensions[j][0]])
                    if y_diff > 0:
                        co_edge_y = corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_basic_id()[j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_corridor_id()[i],
                                      self.get_basic_id()[j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_corridor_conjunct_adjacency(self):
        adjacency = []
        n = len(self.get_corridor_id())
        m = len(self.get_conjunct_id())
        corridor_coordinates = self.get_corridor_coordinates()
        conjunct_coordinates = self.get_conjunct_coordinates()
        corridor_dimensions = self.get_corridor_dimensions()
        conjunct_dimensions = self.get_conjunct_dimensions()
        eps = 1e-4
        for i in range(0, n):
            for j in range(0, m):
                x_diff = corridor_coordinates[i][0] - conjunct_coordinates[j][0]
                a = abs(x_diff) - 0.5 * (corridor_dimensions[i][0] + conjunct_dimensions[j][0])
                y_diff = corridor_coordinates[i][1] - conjunct_coordinates[j][1]
                b = abs(y_diff) - 0.5 * (corridor_dimensions[i][1] + conjunct_dimensions[j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1],
                                        corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1],
                                        conjunct_coordinates[j][1] + 0.5 * conjunct_dimensions[j][1],
                                        conjunct_coordinates[j][1] - 0.5 * conjunct_dimensions[j][1]])
                    if x_diff > 0:
                        co_edge_x = corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0],
                                        corridor_coordinates[i][0] + 0.5 * corridor_dimensions[i][0],
                                        conjunct_coordinates[j][0] + 0.5 * conjunct_dimensions[j][0],
                                        conjunct_coordinates[j][0] - 0.5 * conjunct_dimensions[j][0]])
                    if y_diff > 0:
                        co_edge_y = corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_conjunct_id()[j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_corridor_id()[i],
                                      self.get_conjunct_id()[j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_corridor_adjacency(self):
        adjacency = []
        n = len(self.get_corridor_id())
        corridor_coordinates = self.get_corridor_coordinates()
        corridor_dimensions = self.get_corridor_dimensions()
        eps = 1e-4
        for i in range(0, n - 1):
            for j in range(1, n - i):
                x_diff = corridor_coordinates[i][0] - corridor_coordinates[i + j][0]
                a = abs(x_diff) - 0.5 * (corridor_dimensions[i][0] + corridor_dimensions[i + j][0])
                y_diff = corridor_coordinates[i][1] - corridor_coordinates[i + j][1]
                b = abs(y_diff) - 0.5 * (corridor_dimensions[i][1] + corridor_dimensions[i + j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1],
                                        corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1],
                                        corridor_coordinates[i + j][1] + 0.5 * corridor_dimensions[i + j][1],
                                        corridor_coordinates[i + j][1] - 0.5 * corridor_dimensions[i + j][1]])
                    if x_diff > 0:
                        co_edge_x = corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_corridor_id()[i + j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = corridor_coordinates[i][0] + 0.5 * corridor_dimensions[i][0]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_corridor_id()[i + j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([corridor_coordinates[i][0] - 0.5 * corridor_dimensions[i][0],
                                        corridor_coordinates[i][0] + 0.5 * corridor_dimensions[i][0],
                                        corridor_coordinates[i + j][0] + 0.5 * corridor_dimensions[i + j][0],
                                        corridor_coordinates[i + j][0] - 0.5 * corridor_dimensions[i + j][0]])
                    if y_diff > 0:
                        co_edge_y = corridor_coordinates[i][1] - 0.5 * corridor_dimensions[i][1]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_corridor_id()[i + j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = corridor_coordinates[i][1] + 0.5 * corridor_dimensions[i][1]
                        adjacency.append([self.get_corridor_id()[i],
                                          self.get_corridor_id()[i + j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_corridor_id()[i],
                                      self.get_corridor_id()[i + j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_basic_adjacency(self):
        adjacency = []
        n = len(self.get_basic_id())
        basic_coordinates = self.get_basic_coordinates()
        basic_dimensions = self.get_basic_dimensions()
        eps = 1e-4
        for i in range(0, n - 1):
            for j in range(1, n - i):
                x_diff = basic_coordinates[i][0] - basic_coordinates[i + j][0]
                a = abs(x_diff) - 0.5 * (basic_dimensions[i][0] + basic_dimensions[i + j][0])
                y_diff = basic_coordinates[i][1] - basic_coordinates[i + j][1]
                b = abs(y_diff) - 0.5 * (basic_dimensions[i][1] + basic_dimensions[i + j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([basic_coordinates[i][1] + 0.5 * basic_dimensions[i][1],
                                        basic_coordinates[i][1] - 0.5 * basic_dimensions[i][1],
                                        basic_coordinates[i + j][1] + 0.5 * basic_dimensions[i + j][1],
                                        basic_coordinates[i + j][1] - 0.5 * basic_dimensions[i + j][1]])
                    if x_diff > 0:
                        co_edge_x = basic_coordinates[i][0] - 0.5 * basic_dimensions[i][0]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_basic_id()[i + j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = basic_coordinates[i][0] + 0.5 * basic_dimensions[i][0]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_basic_id()[i + j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([basic_coordinates[i][0] - 0.5 * basic_dimensions[i][0],
                                        basic_coordinates[i][0] + 0.5 * basic_dimensions[i][0],
                                        basic_coordinates[i + j][0] + 0.5 * basic_dimensions[i + j][0],
                                        basic_coordinates[i + j][0] - 0.5 * basic_dimensions[i + j][0]])
                    if y_diff > 0:
                        co_edge_y = basic_coordinates[i][1] - 0.5 * basic_dimensions[i][1]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_basic_id()[i + j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = basic_coordinates[i][1] + 0.5 * basic_dimensions[i][1]
                        adjacency.append([self.get_basic_id()[i],
                                          self.get_basic_id()[i + j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_basic_id()[i],
                                      self.get_basic_id()[i + j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_conjunct_adjacency(self):
        adjacency = []
        n = len(self.get_conjunct_id())
        conjunct_coordinates = self.get_conjunct_coordinates()
        conjunct_dimensions = self.get_conjunct_dimensions()
        eps = 1e-4
        for i in range(0, n - 1):
            for j in range(1, n - i):
                x_diff = conjunct_coordinates[i][0] - conjunct_coordinates[i + j][0]
                a = abs(x_diff) - 0.5 * (conjunct_dimensions[i][0] + conjunct_dimensions[i + j][0])
                y_diff = conjunct_coordinates[i][1] - conjunct_coordinates[i + j][1]
                b = abs(y_diff) - 0.5 * (conjunct_dimensions[i][1] + conjunct_dimensions[i + j][1])
                if abs(a) <= eps and b < 0:
                    co_edge_y = sorted([conjunct_coordinates[i][1] + 0.5 * conjunct_dimensions[i][1],
                                        conjunct_coordinates[i][1] - 0.5 * conjunct_dimensions[i][1],
                                        conjunct_coordinates[i + j][1] + 0.5 * conjunct_dimensions[i + j][1],
                                        conjunct_coordinates[i + j][1] - 0.5 * conjunct_dimensions[i + j][1]])
                    if x_diff > 0:
                        co_edge_x = conjunct_coordinates[i][0] - 0.5 * conjunct_dimensions[i][0]
                        adjacency.append([self.get_conjunct_id()[i],
                                          self.get_conjunct_id()[i + j],
                                          1,
                                          "right&left",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                    if x_diff < 0:
                        co_edge_x = conjunct_coordinates[i][0] + 0.5 * conjunct_dimensions[i][0]
                        adjacency.append([self.get_conjunct_id()[i],
                                          self.get_conjunct_id()[i + j],
                                          1,
                                          "left&right",
                                          (round(co_edge_x), round(co_edge_y[1])),
                                          (round(co_edge_x), round(co_edge_y[2]))])
                elif abs(b) <= eps and a < 0:
                    co_edge_x = sorted([conjunct_coordinates[i][0] - 0.5 * conjunct_dimensions[i][0],
                                        conjunct_coordinates[i][0] + 0.5 * conjunct_dimensions[i][0],
                                        conjunct_coordinates[i + j][0] + 0.5 * conjunct_dimensions[i + j][0],
                                        conjunct_coordinates[i + j][0] - 0.5 * conjunct_dimensions[i + j][0]])
                    if y_diff > 0:
                        co_edge_y = conjunct_coordinates[i][1] - 0.5 * conjunct_dimensions[i][1]
                        adjacency.append([self.get_conjunct_id()[i],
                                          self.get_conjunct_id()[i + j],
                                          1,
                                          "up&down",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                    if y_diff < 0:
                        co_edge_y = conjunct_coordinates[i][1] + 0.5 * conjunct_dimensions[i][1]
                        adjacency.append([self.get_conjunct_id()[i],
                                          self.get_conjunct_id()[i + j],
                                          1,
                                          "down&up",
                                          (round(co_edge_x[1]), round(co_edge_y)),
                                          (round(co_edge_x[2]), round(co_edge_y))])
                else:
                    adjacency.append([self.get_conjunct_id()[i],
                                      self.get_conjunct_id()[i + j],
                                      0,
                                      "no_adjacency",
                                      (0, 0),
                                      (0, 0)])
        return adjacency

    def get_walls_to_down(self, x):
        walls_to_down = list(filter(lambda wall:
                                    round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[0]) == x and
                                    wall.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios
                                    == (0.0, -1.0, 0.0) and
                                    round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                    == round(self.house_level[0].Elevation),
                                    self.walls))
        return walls_to_down

    def get_walls_to_up(self, x):
        walls_to_up = list(filter(lambda wall:
                                  round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[0]) == x and
                                  wall.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios
                                  == (0.0, 1.0, 0.0) and
                                  round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                  == round(self.house_level[0].Elevation),
                                  self.walls))
        return walls_to_up

    def get_walls_to_left(self, y):
        walls_to_left = list(filter(lambda wall:
                                    round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) == y and
                                    wall.ObjectPlacement.RelativePlacement.RefDirection is not None and
                                    round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                    == round(self.house_level[0].Elevation),
                                    self.walls))  # (-1.0, 0.0, 0.0)
        return walls_to_left

    def get_walls_to_right(self, y):
        walls_to_right = list(filter(lambda wall:
                                     round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) == y and
                                     wall.ObjectPlacement.RelativePlacement.RefDirection is None and
                                     round(
                                         wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                     == round(self.house_level[0].Elevation),
                                     self.walls))  # (1.0, 0.0, 0.0)
        return walls_to_right

    def get_corridor_house_connectivity(self):
        corridor_id = self.get_corridor_id()
        corridor_basic_adjacency = self.get_corridor_basic_adjacency()
        corridor_conjunct_adjacency = self.get_corridor_conjunct_adjacency()
        connectivity = []
        h_adjacency = []
        v_adjacency = []
        for c_id in corridor_id:
            h_adjacency += list(filter(lambda element: element[0] == c_id and
                                                       (element[3] == 'right&left' or element[3] == 'left&right'),
                                       corridor_basic_adjacency + corridor_conjunct_adjacency))

            v_adjacency += list(filter(lambda element: element[0] == c_id and
                                                       (element[3] == 'up&down' or element[3] == 'down&up'),
                                       corridor_basic_adjacency + corridor_conjunct_adjacency))

        for h in h_adjacency:
            walls_to_down = self.get_walls_to_down(h[4][0])
            for w in walls_to_down:
                opening = list(filter(lambda op:
                                      h[4][1] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] -
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= h[5][1],
                                      w.HasOpenings))
                if opening:
                    connectivity.append([h[0], h[1], 1])

            walls_to_up = self.get_walls_to_up(h[4][0])
            for w in walls_to_up:
                opening = list(filter(lambda op:
                                      h[4][1] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] +
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= h[5][1],
                                      w.HasOpenings))
                if opening:
                    connectivity.append([h[0], h[1], 1])

        for v in v_adjacency:
            walls_to_left = self.get_walls_to_left(v[4][1])
            for w in walls_to_left:
                opening = list(filter(lambda op:
                                      v[4][0] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] -
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= v[5][0],
                                      w.HasOpenings))
                if opening:
                    connectivity.append([v[0], v[1], 1])
                # for o in w.HasOpenings:
                #     o_x = w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] - \
                #           o.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                #     if v[4][0] <= o_x <= v[5][0]:
                #         connectivity.append([v[0], v[1], 1])

            walls_to_right = self.get_walls_to_right(v[4][1])
            for w in walls_to_right:
                opening = list(filter(lambda op:
                                      v[4][0] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] +
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= v[5][0],
                                      w.HasOpenings))
                if opening:
                    connectivity.append([v[0], v[1], 1])

        return connectivity

    def get_house_connectivity(self):  # 200的内墙宽没改
        connectivity = []
        h_adjacency = []
        v_adjacency = []
        basic_id = self.get_basic_id()
        conjunct_id = self.get_conjunct_id()
        basic_adjacency = self.get_basic_adjacency()
        conjunct_adjacency = self.get_conjunct_adjacency()
        basic_conjunct_adjacency = self.get_basic_conjunct_adjacency()

        for house_id in basic_id + conjunct_id:
            h_adjacency += list(filter(lambda element: element[0] == house_id and
                                                       (element[3] == 'right&left' or element[3] == 'left&right'),
                                       basic_adjacency + conjunct_adjacency + basic_conjunct_adjacency))
            v_adjacency += list(filter(lambda element: element[0] == house_id and
                                                       (element[3] == 'up&down' or element[3] == 'down&up'),
                                       basic_adjacency + conjunct_adjacency + basic_conjunct_adjacency))
        for h in h_adjacency:
            walls_to_down = self.get_walls_to_down(h[4][0])
            walls_to_up = self.get_walls_to_up(h[4][0])
            a_list = []
            for w in walls_to_down + walls_to_up:
                if w in walls_to_down:
                    a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] -
                                         w.Representation.Representations[1].Items[0].SweptArea.XDim),
                                   round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1])))
                elif w in walls_to_up:
                    a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1]),
                                   round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] +
                                         w.Representation.Representations[1].Items[0].SweptArea.XDim)))
            sorted_list = sorted(a_list)
            m = 0
            for w in walls_to_down:
                opening = list(filter(lambda op:
                                      h[4][1] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] -
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= h[5][1],
                                      w.HasOpenings))
                if opening:
                    m = 1
                    connectivity.append([h[0], h[1], 1])
                    break
            for w in walls_to_up:
                opening = list(filter(lambda op:
                                      h[4][1] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] +
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= h[5][1],
                                      w.HasOpenings))
                if opening:
                    m = 1
                    connectivity.append([h[0], h[1], 1])
                    break
            if m == 1:
                continue

            n = []
            x = []
            # 如果只有一条墙且覆盖了邻接线
            if len(sorted_list) == 1 and \
                    sorted_list[0][0] <= h[4][1] + 200 / 2 and \
                    sorted_list[0][1] >= h[5][1] - 200 / 2:
                connectivity.append([h[0], h[1], 0])
                continue
            elif len(sorted_list) > 1:
                # 如果有多条墙，其中任意一条覆盖了邻接线
                for i in range(len(sorted_list)):
                    if sorted_list[i][0] <= h[4][1] + 200 / 2 and sorted_list[i][1] >= h[5][1] - 200 / 2:
                        x.append(1)
                # 如果有多条墙，他们尾首拼接覆盖了邻接线
                for i in range(len(sorted_list) - 1):
                    if ((h[4][1] - 200 / 2 < sorted_list[i][1] < sorted_list[i + 1][0] < h[5][1] + 200 / 2 or
                         h[4][1] - 200 / 2 <= sorted_list[i][1] < sorted_list[i + 1][0] < h[5][1] + 200 / 2 or
                         h[4][1] - 200 / 2 < sorted_list[i][1] < sorted_list[i + 1][0] <= h[5][1] + 200 / 2) and
                            (sorted_list[0][0] <= h[4][1] + 200 / 2 and sorted_list[-1][1] >= h[5][1] - 200 / 2)):
                        if 0 < sorted_list[i + 1][0] - sorted_list[i][1] <= 200:
                            n.append(0)
                        else:
                            n.append(1)
            if x:
                connectivity.append([h[0], h[1], 0])
                continue
            if n != [] and 1 not in n:
                connectivity.append([h[0], h[1], 0])
                continue
            # 剩余循环的邻接关系均为连通关系
            connectivity.append([h[0], h[1], 1])

        for v in v_adjacency:
            walls_to_left = self.get_walls_to_left(v[4][1])
            walls_to_right = self.get_walls_to_right(v[4][1])
            a_list = []
            for w in walls_to_left + walls_to_right:
                if w in walls_to_left:
                    a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] -
                                         w.Representation.Representations[1].Items[0].SweptArea.XDim),
                                   round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0])))
                elif w in walls_to_right:
                    a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0]),
                                   round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] +
                                         w.Representation.Representations[1].Items[0].SweptArea.XDim)))
            sorted_list = sorted(a_list)
            m = 0
            for w in walls_to_left:
                opening = list(filter(lambda op:
                                      v[4][0] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] -
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= v[5][0],
                                      w.HasOpenings))
                if opening:
                    m = 1
                    connectivity.append([v[0], v[1], 1])
                    break
            for w in walls_to_right:
                opening = list(filter(lambda op:
                                      v[4][0] <=
                                      w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] +
                                      op.RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates[0]
                                      <= v[5][0],
                                      w.HasOpenings))
                if opening:
                    m = 1
                    connectivity.append([v[0], v[1], 1])
                    break
            if m == 1:
                continue
            n = []
            x = []
            # 如果只有一条墙且覆盖了邻接线
            if len(sorted_list) == 1 \
                    and sorted_list[0][0] <= v[4][0] + 200 / 2 \
                    and sorted_list[0][1] >= v[5][0] - 200 / 2:
                connectivity.append([v[0], v[1], 0])
                continue
            elif len(sorted_list) > 1:
                # 如果有多条墙，其中任意一条覆盖了邻接线
                for i in range(len(sorted_list)):
                    if sorted_list[i][0] <= v[4][0] + 200 / 2 and sorted_list[i][1] >= v[5][0] - 200 / 2:
                        x.append(1)
                # 如果有多条墙，他们尾首拼接覆盖了邻接线
                for i in range(len(sorted_list) - 1):
                    if ((v[4][0] - 200 / 2 < sorted_list[i][1] < sorted_list[i + 1][0] < v[5][0] + 200 / 2 or
                         v[4][0] - 200 / 2 <= sorted_list[i][1] < sorted_list[i + 1][0] < v[5][0] + 200 / 2 or
                         v[4][0] - 200 / 2 < sorted_list[i][1] < sorted_list[i + 1][0] <= v[5][0] + 200 / 2) and
                            (sorted_list[0][0] <= v[4][0] + 200 / 2 and sorted_list[-1][1] >= v[5][0] - 200 / 2)):
                        if 0 < sorted_list[i + 1][0] - sorted_list[i][1] <= 200:
                            n.append(0)
                        else:
                            n.append(1)
            if x:
                connectivity.append([v[0], v[1], 0])
                continue

            if n != [] and 1 not in n:
                connectivity.append([v[0], v[1], 0])
                continue
            # 剩余循环的邻接关系均为连通关系
            connectivity.append([v[0], v[1], 1])

        return list(filter(lambda a: a[2] == 1, connectivity))
