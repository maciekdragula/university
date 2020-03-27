from queue import *
from copy import deepcopy
from random import choice

#######################################################################################################
#
# Helpers
#
#######################################################################################################

def findAll(state, t):
    # find all positions of either 'G', 'S', 'B' or '#'
    N = len(state[0])
    stringState = ''.join([elem for sublist in state for elem in sublist])
    return {(i%N, i//N) for i in range(len(stringState)) if stringState[i] == t}


def possMoves(walls, posX, posY):
    #assuming that you can't go beyond a gird
    steps = frozenset({(0, 1), (0, -1), (1, 0), (-1, 0)})
    return {(a, b) for (a, b) in steps if (a + posX, b + posY) not in walls}

def cloestGoal(goals, walls, posX, posY):
    # search the cloeast goal on a grid for a soldier
    if (posX, posY) in goals:
        return 0
    Q = Queue()
    Q.put((posX, posY, 0))
    vis = {(posX, posY)}
    while Q.empty() == False:
        posX, posY, dist = Q.get()
        for (a, b) in possMoves(walls, posX, posY):
            if (posX + a, posY + b) in goals:
                return dist + 1
            if (posX + a, posY + b) not in vis:
                vis.add((posX + a, posY + b))
                Q.put((posX + a, posY + b, dist + 1))
    return int(10e6) # means impossible

#######################################################################################################
#
# A* algorithm
#
#######################################################################################################

def aStar(state):
    moves = {(0, 1) : 'D', (0, -1) : 'U', (1, 0) : 'R', (-1, 0) : 'L'}
    N = len(state[0])
    M = len(state)
    both = findAll(state, 'B')
    starts = findAll(state, 'S') | both
    goals = findAll(state, 'G') | both
    walls = frozenset(findAll(state, '#'))
    available = frozenset(findAll(state, '.') | starts | goals)
    starts = frozenset(starts)
    goals = frozenset(goals)
    dist = {(i, j): cloestGoal(goals, walls, i, j) for (i, j) in available}
    s = sum({dist[(x, y)] for (x, y) in starts})
    vis = {starts : 0}
    Q = PriorityQueue()
    Q.put((s, starts, ''))
    while Q.empty() == False:
        _, positions, path = Q.get()
        if positions <= goals:
            return path
        for (a, b) in moves:
            newPositions = frozenset({(x, y) if (x + a, y + b) in walls else (x + a, y + b) for (x, y) in positions})
            s = sum({dist[(x, y)] for (x, y) in newPositions})
            if newPositions not in vis or len(path) + 1 < vis[newPositions]:
                vis[newPositions] = len(path) + 1
                Q.put((s + len(path) + 1, newPositions, path + moves[(a, b)]))
    return 'IMPOSSIBLE'

#######################################################################################################
#
# tests
#
#######################################################################################################

def solve():
    test = []
    for line in open('zad_input.txt'):
        test.append(list(line[:-1].replace(' ', '.')))
    output = str(aStar(test))
    f = open('zad_output.txt', 'w+')
    f.write(output)
    f.close()
    return


solve()
