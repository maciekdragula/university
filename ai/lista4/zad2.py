from random import choice
from time import time

# 1 - Rat
# 2 - Cat
# 3 - Dog
# 4 - Wolf
# 5 - Leopard
# 6 - Tiger
# 7 - Lion
# 8 - Elephant


class Board:
	def __init__(self):
		self.lakes = {(2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (5, 4), (5, 5), (5, 6), (6, 4), (6, 5), (6, 6)}
		self.whiteBase = (4, 1)
		self.blackBase = (4, 9)
		self.Traps = {(3, 1), (5, 1), (4, 2), (3, 9), (4, 8), (5, 9)}
		self.whiteAnimals = {(1, 1) : 6, (7, 1) : 7, (2, 2) : 3, (6, 2) : 2, (1, 3) : 8, (3, 3) : 4, (5, 3) : 5, (7, 3) : 1}
		self.blackAnimals = {(1, 9) : 7, (7, 9) : 6, (2, 8) : 2, (6, 8) : 3, (1, 7) : 1, (3, 7) : 5, (5, 7) : 4, (7, 7) : 8}
		self.lastAttack = 0
		self.mctsStates = {}

	def copy(self):
		newBoard = Board()
		newBoard.whiteAnimals = self.whiteAnimals.copy()
		newBoard.blackAnimals = self.blackAnimals.copy()
		newBoard.lastAttack = self.lastAttack
		return newBoard


	def around(self, x, y):
		res = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
		return set(filter(lambda x : 0 < x[0] < 8 and 0 < x[1] < 10, res))

	def availableMoves(self, x, y, player):
		myAnimals = self.whiteAnimals if player == 1 else self.blackAnimals
		oppAnimals = self.blackAnimals if player == -1 else self.blackAnimals
		myBase = self.whiteBase if player == 1 else self.blackBase
		res = self.around(x, y) - {k for k, v in myAnimals.items()} - {myBase}
		animalType = myAnimals[(x, y)]
		cannotBeat = {k for k, v in oppAnimals.items() if v > animalType and k not in self.Traps}
		if animalType == 1:
			if (x, y) in self.lakes:
				res -= {k for k, v in oppAnimals.items()}
			posEle = (0, 0)
			for k in cannotBeat:
				if k in oppAnimals and oppAnimals[k] == 8:
					posEle = k
			cannotBeat.discard(posEle)
		res -= cannotBeat
		if animalType == 6 or animalType == 7:
			toAdd = set()
			for (u, v) in res:
				if (u, v) in self.lakes:
					du, dv = u - x, v - y
					while (u, v) in self.lakes:
						if (u, v) in oppAnimals and oppAnimals[(u, v)] == 1:
							break
						u += du
						v += dv
					if (u, v) in oppAnimals and (oppAnimals[(u, v)] == 1 or oppAnimals[(u, v)] > animalType):
						continue
					elif (u, v) in myAnimals:
						continue
					else:
						toAdd.add((u, v))
			res |= toAdd
		if animalType != 1:
			res -= self.lakes
		return res

	def randomBot(self, player):
		animals = self.blackAnimals.keys() if player == -1 else self.whiteAnimals.keys()
		allMoves = {}
		for (x, y) in animals:
			possible = self.availableMoves(x, y, player)
			if possible != set():
				allMoves[(x, y)] = frozenset(possible)
		if allMoves != {}:
			chosenAnimal = choice(list(allMoves.keys()))
			chosenMove = choice(list(allMoves[chosenAnimal]))
			return chosenAnimal, chosenMove
		else:
			return (None, None), (None, None)

	def moveAnimal(self, oldX, oldY, newX, newY, player):
		if (oldX, oldY, newX, newY) == (None, None, None, None):
			return 0
		myAnimals = self.whiteAnimals if player == 1 else self.blackAnimals
		oppAnimals = self.blackAnimals if player == 1 else self.whiteAnimals
		oppBase = self.blackBase if player == 1 else self.whiteBase
		if (newX, newY) in oppAnimals:
			# print('here')
			self.lastAtatck = 0
			del oppAnimals[(newX, newY)]
		else:
			self.lastAttack += 1
		myAnimals[(newX, newY)] = myAnimals[(oldX, oldY)]
		del myAnimals[(oldX, oldY)]
		if (newX, newY) == oppBase or oppAnimals == {}:
			return player
		return 0

	def taxiPlayer(self, player):
		animals = self.whiteAnimals.keys() if player == 1 else self.blackAnimals.keys()
		(baseX, baseY) = self.blackBase if player == 1 else self.whiteBase
		bothKeys = self.whiteAnimals.keys() | self.blackAnimals.keys()
		if player == 1:
			if (3, 3) in self.whiteAnimals and self.whiteAnimals[(3, 3)] == 4 and (3, 2) not in bothKeys:
				return (3, 3), (3, 2)
			for (x, y) in {(1, 3), (2, 3), (3, 3)}:
				if (x, y) in self.whiteAnimals and self.whiteAnimals[(x, y)] == 8 and (x + 1, y) not in bothKeys:
					return (x, y), (x + 1, y)
		if player == -1:
			if (5, 7) in self.blackAnimals and self.blackAnimals[(5, 7)] == 4 and (5, 8) not in bothKeys:
				return (5, 7), (5, 8)
			for (x, y) in {(7, 7), (6, 7), (5, 7)}:
				if (x, y) in self.blackAnimals and self.blackAnimals[(x, y)] == 8 and (x - 1, y) not in bothKeys:
					return (x, y), (x - 1, y)
		bestMove = (None, None), (None, None)
		bestDist = 100
		for (x, y) in animals:
			for (u, v) in frozenset(self.availableMoves(x, y, player)):
				d = abs(u - baseX) + abs(v - baseY)
				bestMove = ((x, y), (u, v)) if d < bestDist else bestMove
				bestDist = min(bestDist, d)
		return bestMove

	def MCTS20000(self, player):
		animals = self.whiteAnimals.keys() if player == 1 else self.blackAnimals.keys()
		allMoves = {}
		n = 0
		for (x, y) in animals:
			possible = frozenset(self.availableMoves(x, y, player))
			allMoves[(x, y)] = possible
			n += len(possible)
		bestMove = (None, None), (None, None)
		maxratio = -1
		stepsPerGame = 20000 // (6*n)
		# print("game")
		for (x, y) in allMoves.keys():
			for (u, v) in allMoves[(x, y)]:
				wins = 0
				for i in range(6):
					mctsGame = self.copy()
					mctsGame.moveAnimal(x, y, u, v, player)
					wins += mctsGame.randomPlay(player, stepsPerGame)
				bestMove = ((x, y), (u, v)) if wins/6 > maxratio else bestMove
				maxratio = max(maxratio, wins/6)
		return bestMove

	def decideWhoWins(self):
		wAnim = sorted(list(self.whiteAnimals.values()), reverse = True)
		bAnim = sorted(list(self.whiteAnimals.values()), reverse = True)
		if wAnim != bAnim:
			if wAnim > bAnim:
				return 1
			else:
				return -1
		else:
			f1 = lambda x : abs(x[0] - self.blackBase[0]) + abs(x[1] - self.blackBase[1])
			f2 = lambda x : abs(x[0] - self.whiteBase[0]) + abs(x[1] - self.whiteBase[1])
			wDists = min({f1(x) for x in self.whiteAnimals.keys()})
			bDists = min({f2(x) for x in self.blackAnimals.keys()})
			if wDists < bDists:
				return 1
			elif bDists < wDists:
				return -1
			else:
				return 0

	def randomPlay(self, player, stepsPerGame = 1000000):
		startingPlayer = player
		while stepsPerGame > 0:
			(oldX, oldY), (newX, newY) = self.randomBot(player)
			n = self.moveAnimal(oldX, oldY, newX, newY, player)
			if n != 0:
				return n
			if self.lastAttack == 50:
				break
			player *= -1
			stepsPerGame -= 1
		d = self.decideWhoWins()
		if d != 0:
			return d
		else:
			return -startingPlayer

	def play(self, player):
		self.lastAttack = 0
		startingPlayer = player
		while True:
			(oldX, oldY), (newX, newY) = self.MCTS20000(player) if player == 1 else self.taxiPlayer(player)
			n = self.moveAnimal(oldX, oldY, newX, newY, player)
			if n != 0:
				return n
			if self.lastAttack == 50:
				d = self.decideWhoWins()
				if d != 0:
					return d
				else:
					return -startingPlayer
			player *= -1



def match():
	start = time()
	wins = 0
	losses = 0
	for i in range(100):
		newGame = Board()
		print("Game ", i)
		player = 1 if i%2 == 1 else -1
		if newGame.play(player) > 0:
			wins += 1
		else:
			losses += 1
		# print(newGame.blackAnimals)
		print('Wins: ', wins)
		print('Losses: ', losses)
		# print(newGame.whiteAnimals)
	end = time()
	print('Time elapsed: ', end - start)

match()
