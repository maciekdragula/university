from queue import *
from copy import deepcopy

#######################################################################################################
#
# Helpers
#
#######################################################################################################

def combineMap(grid):
    # from a list of a list to string
    return ''.join([elem for sublist in grid for elem in sublist])

def splitMap(grid, N):
    # from a string to a list of list
    return [list(grid[i:(i + N)]) for i in range(0, len(grid), N)]

def printMap(grid):
    # print a map
    return '\n'.join(''.join(sublist) for sublist in grid)

def possMoves(grid, posX, posY):
    #assuming that you can't go beyond a gird
    steps = {(0, 1, 0, 2), (0, -1, 0, -2), (1, 0, 2, 0), (-1, 0, -2, 0)}
    moves = set()
    for (a, b, c, d) in steps:
        if grid[posY + a][posX + b] in {'.', 'G'} or \
            (grid[posY + a][posX + b] in {'B', '*'} and grid[posY + c][posX + d] in {'.', 'G'}):
            moves.add((a, b, c, d))
    return moves

def findAllBoxes(state, N, M):
    stringState = combineMap(state)
    return [(i%N, i//N) for i in range(len(stringState)) if stringState[i] in {'B', '*'}]

#######################################################################################################
#
# BFS algorithm
#
#######################################################################################################

def BFS(state, N, M):
    moves = {(0, 1) : 'R', (0, -1) : 'L', (1, 0): 'D', (-1, 0): 'U'}
    comb =  combineMap(state)
    pos = max(comb.find('K'), comb.find('+')) #one of them is definitely -1
    posX, posY = pos%N, pos//N
    toFill = comb.count('G')
    vis = {comb}
    Q = Queue()
    Q.put((state, posX, posY, toFill, ''))
    while Q.empty() == False:
        state, posX, posY, toFill, path = Q.get()
        for (a, b, c, d) in possMoves(state, posX, posY):
            newstate = deepcopy(state)
            #correct a position of man after a move
            newstate[posY + a][posX + b] = '+' if state[posY + a][posX + b] in {'G', '*'} else 'K'
            newstate[posY][posX] = 'G' if state[posY][posX] == '+' else '.'
            newPath = path + moves[(a, b)]
            newToFill = toFill
            #correct a position of box if it was moved and a value of f(x), and check if we are done :)
            if state[posY + a][posX + b] in {'B', '*'}:
                newstate[posY + c][posX + d] = 'B' if state[posY + c][posX + d] == '.' else '*'
                if state[posY + a][posX + b] == '*':
                    if state[posY + c][posX + d] == '.':
                        newToFill += 1
                else:
                    if state[posY + c][posX + d] == 'G':
                        newToFill -= 1
                if newToFill == 0:
                    return newPath
            if combineMap(newstate) not in vis:
                vis.add(combineMap(newstate))
                Q.put((newstate, posX + b, posY + a, newToFill, newPath))
    return 'IMPOSSIBLE'

#######################################################################################################
#
# A* algorithm
#
#######################################################################################################

def cloestGoal(grid, N, posX, posY):
    # search the cloeast goal on a grid for a given box; no other obejcts on a grid
    if grid[posY][posX] in {'G', '+', '*'}:
        return 0
    if grid[posY][posX] == 'W':
        return int(10e6)
    stringState = combineMap(grid).replace('B', '.').replace('*', 'G').replace('K', '.').replace('+', 'G')
    state = splitMap(stringState, N)
    state[posY][posX] = 'B'
    Q = Queue()
    Q.put((state, posX, posY, 0))
    vis = {stringState}
    while Q.empty() == False:
        state, posX, posY, dist = Q.get()
        for (a, b, _, _) in possMoves(state, posX, posY):
            newstate = deepcopy(state)
            if(newstate[posY + a][posX + b] == 'G'):
                return dist + 1
            newstate[posY + a][posX + b], newstate[posY][posX] = newstate[posY][posX], newstate[posY + a][posX + b]
            if combineMap(newstate) not in vis:
                vis.add(combineMap(newstate))
                Q.put((newstate, posX + b, posY + a, dist + 1))
    return int(10e6) # means impossible




def aStar(state, N, M):
    moves = {(0, 1) : 'R', (0, -1) : 'L', (1, 0): 'D', (-1, 0): 'U'}
    comb =  combineMap(state)
    pos = max(comb.find('K'), comb.find('+')) #one of them is definitely -1
    posX, posY = pos%N, pos//N
    toFill = comb.count('G')
    vis = {comb}
    distToGoal = [[0 for x in range(N)] for y in range(M)]
    for i in range(len(comb)):
        x, y = i%N, i//N
        distToGoal[y][x] = cloestGoal(state, N, x, y)
    # calculate an initial value of f(x) = g(x) + h(x)
    f = 0
    for (x, y) in findAllBoxes(state, N, M):
        f += distToGoal[y][x]
    Q = PriorityQueue()
    Q.put((f, state, posX, posY, toFill, ''))
    while Q.empty() == False:
        f, state, posX, posY, toFill, path = Q.get()
        # print(printMap(state), toFill)
        # input()
        for (a, b, c, d) in possMoves(state, posX, posY):
            newstate = deepcopy(state)
            #correct a position of man after a move
            newstate[posY + a][posX + b] = '+' if state[posY + a][posX + b] in {'G', '*'} else 'K'
            newstate[posY][posX] = 'G' if state[posY][posX] == '+' else '.'
            newPath = path + moves[(a, b)]
            newToFill = toFill
            newF = f + 1
            #correct a position of box if it was moved and a value of f(x), and check if we are done :)
            if state[posY + a][posX + b] in {'B', '*'}:
                newstate[posY + c][posX + d] = 'B' if state[posY + c][posX + d] == '.' else '*'
                if state[posY + a][posX + b] == '*':
                    if state[posY + c][posX + d] == '.':
                        newToFill += 1
                else:
                    if state[posY + c][posX + d] == 'G':
                        newToFill -= 1
                if newToFill == 0:
                    return newPath
                newF = newF - distToGoal[posY + a][posX + b] + distToGoal[posY + c][posX + d]
            if combineMap(newstate) not in vis:
                vis.add(combineMap(newstate))
                Q.put((newF, newstate, posX + b, posY + a, newToFill, newPath))
    return 'IMPOSSIBLE'



#######################################################################################################
#
# Main solver
#
#######################################################################################################


def solve():
    test = []
    for line in open('zad_input.txt'):
        test.append(list(line[:-1]))
    output = BFS(test, len(test[0]), len(test))
    f1 = open('zad_output.txt', 'w+')
    f1.write(output)
    f1.close()
    return

solve()
