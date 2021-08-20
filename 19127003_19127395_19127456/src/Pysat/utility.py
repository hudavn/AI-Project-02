from math import comb
from itertools import combinations, permutations
import time
from pysat.solvers import Glucose3
from pysat.card import *

# ==============================================

xCfg = [0, -1, -1, -1, 0, 1, 1, 1, 0]
yCfg = [0, -1, 0, 1, 1, 1, 0, -1, -1]

# ==============================================

def InputData(fileAddr):
    global info, adj, color, clauses, found, nrow, ncol
    info = list(list())
    adj = list(list())
    color = list(list())
    clauses = list()
    found = 0

    f = open(fileAddr, "r")
    
    for line in f:
        info.append(line.split())

    nrow = len(info)
    ncol = len(info[0])

    for i in range(nrow):
        color.append(list())
        adj.append(list())

        for j in range(ncol):
            info[i][j] = int(info[i][j])
            numAdj = 9
            if i == 0 or j == 0 or i == nrow-1 or j == ncol-1:
                if i in (0, nrow-1) and j in (0, ncol-1):
                    numAdj = 4
                else:
                    numAdj = 6

            adj[i].append(numAdj)
            color[i].append(0)

    f.close()

# ==============================================

def makeCNF():
    for i in range(nrow):
        for j in range(ncol):
            if info[i][j] != -1:
                negCons = combinations(
                    [0, 1, 2, 3, 4, 5, 6, 7, 8], adj[i][j] - info[i][j] + 1)
                posCons = combinations(
                    [0, 1, 2, 3, 4, 5, 6, 7, 8], info[i][j] + 1)

                if negCons:
                    for choosen in negCons:
                        clause = list()

                        for k in choosen:
                            X = i + xCfg[k]
                            Y = j + yCfg[k]
                            if (X not in range(nrow)) or (Y not in range(ncol)):
                                break
                            clause.append(ncol * X + Y + 1)

                        clause = sorted(clause)
                        if len(clause) == len(choosen) and clause not in clauses:
                            clauses.append(clause)

                if posCons:
                    for choosen in posCons:
                        clause = list()

                        for k in choosen:
                            X = i + xCfg[k]
                            Y = j + yCfg[k]
                            if (X not in range(nrow)) or (Y not in range(ncol)):
                                break
                            clause.append(-(ncol * X + Y + 1))

                        clause = sorted(clause)
                        if len(clause) == len(choosen) and clause not in clauses:
                            clauses.append(clause)

# ==============================================

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

# ==============================================

def Coloring():
    makeCNF()
    g = Glucose3()

    for item in clauses:
        # print(item)
        g.add_clause(item)

    if g.solve():
        global found
        found = 1
        model = g.get_model()

        for it in model:
            temp = abs(it)
            X = (temp-1) // ncol
            Y = (temp-1) % ncol

            if it > 0:
                color[X][Y] = 1
            else:
                color[X][Y] = 0
