import object as obj
from object import *
from itertools import combinations
import time


def InputData():
    f = open("input.txt", "r")

    for line in f:
        info.append(line.split())

    for i in range(len(info)):
        color.append(list())
        for j in range(len(info[i])):
            info[i][j] = int(info[i][j])
            if (info[i][j]):
                constraint.append((i, j))
            color[i].append(0)

    f.close()


def visualized():
    for row in info:
        for item in row:
            if item == 0:
                print(" . ", end="")
            else:
                print("", item, "", end="")
        print()

    if not obj.found:
        print("NO SOLUTION")
        return

    for i in range(len(info[0])):
        print("===", end="")
    print(" 0 - Red / 1 - Blue")

    for row in color:
        for item in row:
            print("", item, "", end="")
        print()


def SAT():
    for each in constraint:
        temp = 0
        for loop in range(9):
            X = each[0] + xCfg[loop]
            Y = each[1] + yCfg[loop]
            if (X not in range(len(info))) or (Y not in range(len(info[0]))):
                continue
            temp += color[X][Y]
        if temp != info[each[0]][each[1]]:
            return 0

    return 1


def Coloring(id):
    if (time.time() - start) > 600:
        print("NO SOLUTION")
        exit(0)

    if (id == len(info)*len(info[0])):
        if SAT():
            obj.found = 1
        return

    X = id // len(info[0])
    Y = id % len(info[0])

    Coloring(id + 1)
    if obj.found:
        return

    color[X][Y] = 1

    Coloring(id + 1)
    if obj.found:
        return

    color[X][Y] = 0
