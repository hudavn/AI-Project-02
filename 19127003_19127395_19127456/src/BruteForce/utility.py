from itertools import combinations
import time

# ================================================

xCfg = [0, -1, -1, -1, 0, 1, 1, 1, 0]
yCfg = [0, -1, 0, 1, 1, 1, 0, -1, -1]

# ================================================

def InputData(fileAddr):
    
    global info, color, constraint, found, start
    info = list(list())
    color = list(list())
    constraint = list()
    found = 0
    start = time.time()
    
    f = open(fileAddr, "r")

    for line in f:
        info.append(line.split())

    for i in range(len(info)):
        color.append(list())

        for j in range(len(info[i])):
            info[i][j] = int(info[i][j])

            if info[i][j] != -1:
                constraint.append((i, j))

            color[i].append(0)

    f.close()

# ================================================

def visualized():
    for row in info:
        for item in row:
            if item == -1:
                print(" . ", end="")
            else:
                print("", item, "", end="")
        print()

    for i in range(len(info[0])):
        print("===", end="")

    if not found:
        print("NO SOLUTION")
        return 

    print(" 0 - Red / 1 - Blue")

    for row in color:
        for item in row:
            print("", item, "", end="")
        print()

# ================================================

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

# ================================================

def Coloring(id):
    global found, start
    
    if (time.time() - start) > 600:
        print("NO SOLUTION")
        exit(0)

    if (id == len(info)*len(info[0])):
        if SAT():
            found = 1
        return

    X = id // len(info[0])
    Y = id % len(info[0])

    Coloring(id + 1)
    if found:
        return

    color[X][Y] = 1

    Coloring(id + 1)
    if found:
        return

    color[X][Y] = 0
