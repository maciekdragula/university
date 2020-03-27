from random import choice
from copy import deepcopy
from time import time



class Board:


    def __init__(self):
        self.white = {(4, 5), (5, 4)}
        self.black = {(4, 4), (5, 5)}
        ls = [
               [1000, -50, 100, 100, 100, 100,  -50, 1000],
               [-50, -200,   1,   1,   1,   1, -200,  -50],
               [100,    1,   1,   1,   1,   1,    1,  100],
               [100,    1,   1,   0,   0,   1,    1,  100],
               [100,    1,   1,   0,   0,   1,    1,  100],
               [100,    1,   1,   1,   1,   1,    1,  100],
               [-50, -200,   1,   1,   1,   1, -200,  -50],
               [1000, -50, 100, 100, 100, 100,  -50, 1000]
             ]
        self.available = {(6, 3), (6, 4), (6, 5), (6, 6), (5, 6), (4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3)}
        self.weigths = {(i + 1, j + 1) : ls[i][j] for i in range(8) for j in range(8)}

    def around(self, x, y): # zwraca listę pól dookoła (x, y); uważa, żeby nie wyjechać poza planszę
        tmp = {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}
        return set(filter(lambda x : 0 < x[0] < 9 and 0 < x[1] < 9, tmp))

    def canBeat(self, x, y, player): # zwraca True jeśli gracz player ma bicie stawiając pionek na polu(x, y); wpp False
        myDisks = self.black if player == 1 else self.white
        oppDisks = self.white if player == 1 else self.black
        neighOppDisks = self.around(x, y) & oppDisks
        for (a, b) in neighOppDisks:
            du, dv = a - x, b - y
            u, v = x, y
            steps = 0
            while (u + du, v + dv) in oppDisks:
                steps += 1
                u += du
                v += dv
            if steps > 0 and (u + du, v + dv) in myDisks:
                return True
        return False

    def correctCorner(self, x, y, justAdded):
        if (x, y) not in {(1, 1), (8, 8), (1, 8), (8, 1)}:
            return
        if justAdded:
            for (u, v) in self.around(x, y):
                self.weigths[(u, v)] = 20 if abs(u - x) == 1 and abs(v - y) == 1 else 200
        else:
            for(u, v) in self.around(x, y):
                self.weigths[(u, v)] = -200 if abs(u - x) == 1 and abs(v - y) == 1 else -50

    def move(self, x, y, player): # wykonuje ruch gracza player stawiając pionek na polu (x, y)
        myDisks = self.black if player == 1 else self.white
        oppDisks = self.white if player == 1 else self.black
        direction = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
        myDisks.add((x, y))
        self.correctCorner(x, y, True)
        self.available.remove((x, y))
        newAvailable = self.around(x, y) - (self.white | self.black | self.available)
        self.available |= newAvailable
        beaten = set()
        for (du, dv) in direction:
            u, v = x, y
            tmp = set()
            while (u + du, v + dv) in oppDisks:
                u += du
                v += dv
                tmp.add((u, v))
            if (u + du, v + dv) in myDisks:
                beaten |= tmp
        myDisks |= beaten
        oppDisks -= beaten
        return beaten, newAvailable

    def randomMove(self, player): # wykonuje losowy ruch gracza player
        possible = [(x, y) for (x, y) in self.available if self.canBeat(x, y, player)]
        if possible == []:
            self.noMoves += 1
            return
        (x, y) = choice(possible)
        self.move(x, y, player)
        self.noMoves = 0

    def heura(self):
        tmp1 = sum(self.weigths[p] for p in self.black)
        tmp2 = sum(self.weigths[p] for p in self.white)
        return tmp1 - tmp2


    def minn(self, depth, alpha, beta):
        if depth == 1:
            return self.heura(), (9, 9)
        value = 1000000000000
        bestPos = (-1, -1)
        possible = [(x, y) for (x, y) in self.available if self.canBeat(x, y, -1)]
        if possible == []:
            return self.maxx(depth - 1, alpha, beta)
        for (x, y) in possible:
            beaten, newAvailable = self.move(x, y, -1) #  wykonujemy ruch na pozycję (x, y)
            tmpVal, _ = self.maxx(depth - 1, alpha, beta)
            if tmpVal <= value: # sprawdzamy czu poprawiamy value
                value = tmpVal
                bestPos = (x, y)
            self.available -= newAvailable
            self.available.add((x, y))
            self.white.remove((x, y))
            self.white -= beaten
            self.black |= beaten
            self.correctCorner(x, y, False)
            if value <= alpha: # jeśli value jest gorsze od alpha to odcinamy
                return value, bestPos
            beta = min(value, beta)
        return value, bestPos

    def maxx(self, depth, alpha, beta):
        if depth == 1:
            return self.heura(), (9, 9)
        value = -1000000000000
        bestPos = (-1, -1)
        possible = [(x, y) for (x, y) in self.available if self.canBeat(x, y, 1)]
        if possible == []:
            return self.minn(depth - 1, alpha, beta)
        for (x, y) in possible:
            beaten, newAvailable = self.move(x, y, 1) # wykonujemy ruch na pozycję (x, y)
            tmpVal, _ = self.minn(depth - 1, alpha, beta)
            if tmpVal >= value: # sprawdzamy czu poprawiamy value
                value = tmpVal
                bestPos = (x, y)
            self.available -= newAvailable
            self.available.add((x, y))
            self.black.remove((x, y))
            self.black -= beaten
            self.white |= beaten
            self.correctCorner(x, y, False)
            if value >= beta:
                return value, bestPos # jeśli value jest gorsze od alpha to odcinamy
            alpha = max(alpha, value)
        return value, bestPos


    def agentMove(self, player):
        _, bestPosition = self.maxx(4, -1000000000000, 1000000000000) if player == 1 else self.minn(4, -1000000000000, 1000000000000)
        if bestPosition == (-1, -1)  or bestPosition == (9, 9):
            self.noMoves += 1
            return
        (i, j) = bestPosition
        self.move(i, j, player)
        self.noMoves = 0


    def game(self, startingPlayer):
        self.noMoves = 0
        player = 1
        while self.black and self.white and len(self.white) + len(self.black) != 64:
            if self.noMoves == 2:
                break
            if player == startingPlayer:
                self.agentMove(player)
            else:
                self.randomMove(player)
            player *= -1
        return len(self.black) - len(self.white)


def match():
    start = time()
    wins = 0
    losses = 0
    draws = 0
    for i in range(1000): # should be 1000
        startingPlayer = 1 if i%2 == 0 else -1
        newGame = Board()
        # print("Game", i)
        res = newGame.game(startingPlayer) # 1 is agent, -1 is randomAgent
        if res*startingPlayer > 0:
            wins += 1
        elif res*startingPlayer < 0:
            losses += 1
        else:
            draws += 1
    print('Wins: ', wins)
    print('Losses: ', losses)
    print('Draws: ', draws)
    end = time()
    print('Time elapsed: ', end - start)

match()
