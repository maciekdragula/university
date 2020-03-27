with open('data') as slowa:
    words = {word for line in slowa for word in line.split()}

with open('pan_tadeusz_bez_spacji.txt') as panTad:
    S = [verse for line in panTad for verse in line.split()]

#S = ['tamatematykapustkinieznosi']

def maxWordLength():
    maxlen = 0
    for e in words:
        maxlen = max(maxlen, len(e))
    return maxlen

def solve(l, m, S):
    dp = [0]*(l + 1)
    w = ['']*(l + 1)
    for i in range(l):
        if (i != 0 and dp[i] == 0):
             continue
        for j in range(i + 1, min(i + m + 1, l + 1)):
            if S[i:j] in words:
                if dp[j] < dp[i] + (j - i)*(j - i):
                    dp[j] = dp[i] + (j - i)*(j - i)
                    w[j] = S[i:j]
    return w

def findResult(w, l):
    res = []
    while(l > 0):
        res.append(w[l])
        l -= len(w[l])
    return res[::-1]

M = maxWordLength()

for verse in S:
    L = len(verse)
    print(' '.join(findResult(solve(L, M, verse), L)))
