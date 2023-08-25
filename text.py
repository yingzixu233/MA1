import ifcopenshell

# doors = ifcopenshell.open('项目1.ifc').by_type("IfcOpeningElement")
# string1 = "入户门"
# h_doors = list(filter(lambda h_door: h_door.Name.find("入户门") != -1, doors))
# number = len(h_doors)
# print("The total number of doors:", number)
# a = h_doors[0].Representation.Representations[0].Items[0].SweptArea
# for door in doors:
#     b = door.ObjectPlacement.RelativePlacement.Location.Coordinates
#     print(b)

# for door in doors:
#     print(door.get_info())
#
# doors_2 = ifcopenshell.open('项目2.ifc').by_type("IfcDoor")
# print()
# for door in doors_2:
#     print(door.get_info())
#
# wall = ifcopenshell.open('项目1.ifc').by_type("IfcWall")
# # print()
# print(wall[0].get_info())
# for w in wall:
#     print(w)
# print()
# if wall[0].ObjectPlacement.RelativePlacement.RefDirection is not None:
#     print(wall[0])
# else:
#     print("none")
#
# print(wall[1].ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios)
# print(wall[2].ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios)
# print(wall[7].ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios)
# print(wall[7].HasOpenings[0].RelatedOpeningElement.ObjectPlacement.RelativePlacement.Location.Coordinates)
#
# print()
# element = ifcopenshell.open('项目2.ifc').by_type("IfcRelVoidsElement")

# for e in element:
#     if(e.RelatingBuildingElement) RelatedOpeningElement
# print(element[0].RelatingBuildingElement.get_info())

#
# for door in h_doors:
#     print(door.get_info())
#     print(door.Name, ": ", door.ObjectPlacement.RelativePlacement.Location.Coordinates)
#     print()
#
# modules = ifcopenshell.open('MA-Case Study.ifc').by_type("IfcBuildingElementProxy")
# corridor_modules = list(filter(lambda corridor: corridor.ObjectType == '模块:走道模块', modules))
# corridor_coordinates = corridor_modules[0].ObjectPlacement.RelativePlacement.Location.Coordinates
# l = corridor_modules[0].IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue
# w = corridor_modules[0].IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue
# print(corridor_modules[0].ObjectPlacement.RelativePlacement.Location.Coordinates)
#
# print(corridor_modules[0].IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[0].NominalValue.wrappedValue,
#       corridor_modules[0].IsDefinedBy[2].RelatingPropertyDefinition.HasProperties[1].NominalValue.wrappedValue)

# walls = ifcopenshell.open('MA-Case Study.ifc').by_type("IfcWallStandardCase")
#
# w_1 = list(filter(lambda wall: wall.GlobalId == "1gXnag4b51DO085b8Uewuc", walls))
# w_2 = list(filter(lambda wall: wall.GlobalId == "2t746mC715Hu6lDCInouzx", walls))
#
# print(w_1[0].ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
#
# print(w_2[0].ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])


# print(corridor_wall[0].ObjectPlacement.RelativePlacement.Location.Coordinates)
# print(corridor_wall[0].Representation.Representations[1].Items[0].SweptArea.YDim)
# print(corridor_wall[0].Representation.Representations[1].Items[0].SweptArea.XDim)
#
# corridor_wall = list(filter(lambda wall1: round(wall1.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) == 6939,
#                             walls))
# #
# for wall in corridor_wall:
#     print(wall)
#     print(wall.ObjectPlacement.RelativePlacement.Location.Coordinates)
#     print(wall.Representation.Representations[1].Items[0].SweptArea.YDim)
#     print(wall.Representation.Representations[1].Items[0].SweptArea.XDim)
#
#
# # 获取corridor_wall
# corridor_w = list(filter(lambda wl:
#                          (
#                                  round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[0]) ==
#                                  round(corridor_coordinates[0] + l / 2)
#                                  and
#                                  round(corridor_coordinates[1] + w / 2 -
#                                        wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                                  >= round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[1])
#                                  > round(corridor_coordinates[0] - w / 2 -
#                                          wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                          )
#                          or
#                          (
#                                  round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[0]) ==
#                                  round(corridor_coordinates[0] - l / 2)
#                                  and
#                                  round(corridor_coordinates[1] + w / 2 -
#                                        wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                                  >= round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[1])
#                                  > round(corridor_coordinates[0] - w / 2 -
#                                          wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                          )
#                          or
#                          (
#                                  round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) ==
#                                  round(corridor_coordinates[1] + w / 2)
#                                  and
#                                  round(corridor_coordinates[0] - l / 2 +
#                                        wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                                  <= round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[0])
#                                  < round(corridor_coordinates[0] + l / 2 +
#                                          wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                          )
#                          or
#                          (
#                                  round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) ==
#                                  round(corridor_coordinates[1] - w / 2)
#                                  and
#                                  round(corridor_coordinates[0] - l / 2 +
#                                        wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                                  <= round(wl.ObjectPlacement.RelativePlacement.Location.Coordinates[0])
#                                  < round(corridor_coordinates[0] + l / 2 +
#                                          wl.Representation.Representations[1].Items[0].SweptArea.YDim / 2)
#                          )
#                          , walls))

# a = corridor_w[1].HasOpenings
# print(a)
# for c in corridor_w:
#     print(c)

# student_tuples = [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]
# a = sorted(student_tuples, key=lambda student: student[2])
#
# b = list([1, 2, 35, 6, 3])
# m = list(filter(lambda x: x == 2, b))
# print(m[0])

import module_extractor
import ifcopenshell

a = module_extractor.ModuleExtractor('MA-Case Study.ifc')
tube_basic_adjacency = a.get_tube_basic_adjacency()
tube_conjunct_adjacency = a.get_tube_conjunct_adjacency()
tube_corridor_adjacency = a.get_tube_corridor_adjacency()
basic_conjunct_adjacency = a.get_basic_conjunct_adjacency()
corridor_basic_adjacency = a.get_corridor_basic_adjacency()
corridor_conjunct_adjacency = a.get_corridor_conjunct_adjacency()
corridor_adjacency = a.get_corridor_adjacency()
basic_adjacency = a.get_basic_adjacency()
conjunct_adjacency = a.get_conjunct_adjacency()

corridor_id = a.get_corridor_id()
basic_id = a.get_basic_id()
conjunct_id = a.get_conjunct_id()

# connectivity = []
# mm = []
# for h_id in basic_id + conjunct_id:
#     mm += list(filter(lambda element: element[0] == h_id and
#                                      (element[3] == 'right&left' or element[3] == 'left&right'),
#                       basic_adjacency + basic_conjunct_adjacency + conjunct_adjacency))
# for a in mm:
#     print(a)


# for aa in h_adjacency:
#     print(aa)
# for aa in connectivity:
#     print(aa)
# b = []
# for aa in a:
#     if aa[3] == ('right&left' or 'left&right'):
#         b.append(aa)
# for
# filtered_walls = list(filter(lambda wall:
#                              round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[0])
#                              == aa[4][0], walls))
# print(filtered_walls)
# filtered_walls.clear()


storey = ifcopenshell.open('MA-Case Study.ifc').by_type("IfcBuildingStorey")
level = list(filter(lambda l: l.Name == "户型", storey))
print(round(level[0].Elevation))

# #
connectivity = []
h_adjacency = []
v_adjacency = []

b_list = []
walls = ifcopenshell.open('MA-Case Study.ifc').by_type("IfcWallStandardCase")

walls_to_down = []
walls_to_up = []
for house_id in basic_id + conjunct_id:
    h_adjacency += list(filter(lambda element: element[0] == house_id and
                                               (element[3] == 'right&left' or element[3] == 'left&right'),
                               basic_adjacency + conjunct_adjacency + basic_conjunct_adjacency))
    v_adjacency += list(filter(lambda element: element[0] == house_id and
                                               (element[3] == 'up&down' or element[3] == 'down&up'),
                               basic_adjacency + conjunct_adjacency + basic_conjunct_adjacency))
for h in h_adjacency:
    print("左右邻接关系: ", h)
    walls_to_down = list(filter(lambda wall:
                                round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[0]) == h[4][0]
                                and wall.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios
                                == (0.0, -1.0, 0.0)
                                and
                                round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                == round(level[0].Elevation),
                                walls))
    print("walls_to_down:", walls_to_down)
    walls_to_up = list(filter(lambda wall:
                              round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[0]) == h[4][0]
                              and wall.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios
                              == (0.0, 1.0, 0.0)
                              and round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                              == round(level[0].Elevation),
                              walls))
    print("walls_to_up:", walls_to_up)
    a_list = []
    for w in walls_to_down + walls_to_up:
        print(w)
        if w in walls_to_down:
            a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] -
                                 w.Representation.Representations[1].Items[0].SweptArea.XDim),
                           round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1])))
        elif w in walls_to_up:
            a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1]),
                           round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[1] +
                                 w.Representation.Representations[1].Items[0].SweptArea.XDim)))

    print(a_list)
    sorted_list = sorted(a_list)
    print(sorted_list)
    print()

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

    if m == 1:
        continue

    n = []
    x = []
    # 如果只有一条墙且覆盖了邻接线
    if len(sorted_list) == 1 and sorted_list[0][0] <= h[4][1] + 200 / 2 and sorted_list[0][1] >= h[5][1] - 200 / 2:
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
    print("上下邻接关系: ", v)
    walls_to_left = list(filter(lambda wall:
                                round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) == v[4][1] and
                                wall.ObjectPlacement.RelativePlacement.RefDirection is not None and
                                round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                == round(level[0].Elevation),
                                walls))  # (-1.0, 0.0, 0.0)
    print("walls_to_left:", walls_to_left)
    walls_to_right = list(filter(lambda wall:
                                 round(wall.ObjectPlacement.RelativePlacement.Location.Coordinates[1]) == v[4][1] and
                                 wall.ObjectPlacement.RelativePlacement.RefDirection is None and
                                 round(wall.ObjectPlacement.PlacementRelTo.RelativePlacement.Location.Coordinates[2])
                                 == round(level[0].Elevation),
                                 walls))  # (-1.0, 0.0, 0.0)
    print("walls_to_right:", walls_to_right)
    a_list = []
    for w in walls_to_left + walls_to_right:
        print(w)
        if w in walls_to_left:
            a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] -
                                 w.Representation.Representations[1].Items[0].SweptArea.XDim),
                           round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0])))
        elif w in walls_to_right:
            a_list.append((round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0]),
                           round(w.ObjectPlacement.RelativePlacement.Location.Coordinates[0] +
                                 w.Representation.Representations[1].Items[0].SweptArea.XDim)))

    print(a_list)
    sorted_list = sorted(a_list)
    print(sorted_list)
    print()

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
    if len(sorted_list) == 1 and sorted_list[0][0] <= v[4][0] + 200 / 2 and sorted_list[0][1] >= v[5][0] - 200 / 2:
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

for c in connectivity:
    print(c)
