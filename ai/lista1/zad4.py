def opt_dist (ls, d):
	if d > len(ls):
		return 'd cannot be longer than the length of ls'
		#raise ValueError('d cannot be longer than the length of ls')
	res = numChanges = ls[:d].count(0) + ls[d:].count(1)
	for i in range(len(ls) - d):
		if ls[i] != ls[i + d]:
			if ls[i] == 0:
				numChanges -= 2
				res = min(res, numChanges)
			else:
				numChanges += 2
	return res


	

L = [
	([0, 1, 0], 4), #TEST 0
	([1, 1, 1, 1], 4), #TEST 1
	([0, 0, 0, 0], 4), #TEST 2
	([1, 0, 1, 1], 4), #TEST 3
	([0, 1, 1, 0, 1], 4), #TEST 4
	([1, 0, 1, 0, 1], 4), #TEST 5
	([0, 0, 0, 0, 1], 4), #TEST 6
	([1, 0, 0, 0, 1], 4), #TEST 7
	([1, 0, 0, 0, 0, 1], 4), #TEST 8
	([1, 1, 1, 0, 1, 1], 4), #TEST 9
	([1, 1, 1, 1, 1, 0, 0, 0], 4), #TEST 10
	([1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0], 4), #TEST 11
	([1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0], 4), #TEST 12
	([1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0], 4), #TEST 13
	# Tu zaczynają się testy z treści zadania:
	([0, 0, 1, 0, 0, 0, 1, 0, 0, 0,],  5), #TEST 14
	([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 4), #TEST 15
	([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 3), #TEST 16
	([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 2), #TEST 17
	([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 1), #TEST 18
	([0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 0) #TEST 19
]

for num, (ls, d) in enumerate(L):
	print('Test', num, ': ', opt_dist(ls, d))