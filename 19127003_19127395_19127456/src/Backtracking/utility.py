from itertools import combinations
import time

# ================================================


xCfg = [0, -1, -1, -1, 0, 1, 1, 1, 0]
yCfg = [0, -1, 0, 1, 1, 1, 0, -1, -1]


# ================================================


def InputData(fileAddr):
    global info, color, constraint, start, found
    info = list(list())
    color = list(list())
    constraint = list()
    start = time.time()
    found = 0

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

    if (id == len(constraint)):
        if SAT():
            found = 1
        return

    perm = combinations([0, 1, 2, 3, 4, 5, 6, 7, 8],
                        info[constraint[id][0]][constraint[id][1]])

    for each in list(perm):
        changed = list()
        cnt = 0

        for i in range(9):
            nextX = constraint[id][0] + xCfg[i]
            nextY = constraint[id][1] + yCfg[i]

            if (nextX not in range(len(info))) or (nextY not in range(len(info[0]))):
                continue

            if i in each:
                if not color[nextX][nextY]:
                    color[nextX][nextY] = 1
                    changed.append((nextX, nextY))

            cnt += color[nextX][nextY]

        if cnt != len(each):
            for i in changed:
                color[i[0]][i[1]] = 0
            continue

        Coloring(id+1)
        if found:
            return

        for i in changed:
            color[i[0]][i[1]] = 0
