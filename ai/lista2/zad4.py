from queue import *
from copy import deepcopy
from random import choice
import time
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


def randomMoves(starts, walls):
    moves = {(0, 1) : 'D', (0, -1) : 'U', (1, 0) : 'R', (-1, 0) : 'L'}
    while True:
        positions = starts
        path = ''
        for i in range(110):
            (a, b) = choice(list(moves.keys()))
            # może trzeba wywalić to robienie frozenset
            positions = frozenset({(x, y) if (x + a, y + b) in walls else (x + a, y + b) for (x, y) in positions})
            path += moves[(a, b)]
            if len(positions) <= 3:
                return (positions, path)

#######################################################################################################
#
# BFS algorithm
#
#######################################################################################################

def BFS(state):
    moves = {(0, 1) : 'D', (0, -1) : 'U', (1, 0) : 'R', (-1, 0) : 'L'}
    both = findAll(state, 'B')
    starts = frozenset(findAll(state, 'S') | both)
    goals = frozenset(findAll(state, 'G') | both)
    walls = findAll(state, '#')
    if starts <= goals:
        return ''
    (pos, path) = randomMoves(starts, walls)
    vis = {pos}
    Q = Queue()
    Q.put((pos, path))
    while Q.empty() == False:
        pos, path = Q.get()
        for (a, b) in moves:
            newPos = frozenset({(x, y) if (x + a, y + b) in walls else (x + a, y + b) for (x, y) in pos})
            newPath = path + moves[(a, b)]
            if newPos <= goals:
                if len(newPath) > 150:
                    print('here')
                    return BFS(state)
                else:
                    return newPath
            if newPos not in vis:
                vis.add(newPos)
                Q.put((newPos, newPath))
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
    # print(test)
    output = BFS(test)
    f = open('zad_output.txt', 'w+')
    f.write(output)
    f.close()
    return

solve()
