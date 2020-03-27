from random import choice

def generate(cur, rest, freeFields):
    if rest == []:
        return {tuple(cur + freeFields*[-1])}
    S1 = set()
    S2 = set()
    if freeFields >= rest[0] + 1:
        S1 = generate(cur + [-1], rest, freeFields - 1)
    if (cur == [] or cur[-1] == -1) and freeFields >= rest[0]:
        S2 = generate(cur + rest[0]*[1], rest[1:], freeFields - rest[0])
    elif cur != [] and cur[-1] == 1 and freeFields >= rest[0] + 1:
        S2 = generate(cur + [-1] + rest[0]*[1], rest[1:], freeFields - rest[0] - 1)
    return S1 | S2

def andTuple(t1, t2):
    if len(t1) != len(t2):
        return 'Cannot take & on such tuples'
    res = []
    for i in range(len(t1)):
        x = t1[i] if t1[i] == t2[i] else 0
        res.append(x)
    return tuple(res)

def orTuple(t1, t2):
    if len(t1) != len(t2):
        return 'Cannot take | on such tuples'
    res = []
    for i in range(len(t1)):
        x = 1 if t1[i] == 1 or t2[i] == 1 else -1 if t1[i] == -1 or t2[i] == -1 else 0
        res.append(x)
    return tuple(res)

def andSet(S):
    s = choice(list(S))
    for e in S:
        s = andTuple(s, e)
    return s

def revBoard(B, N):
    res = ''
    for i in range(N):
        for j in range(N):
            res += B[i + (N + 1)*j]
        res += '\n'
    return res

def boardToString(rowRes):
    res = ''
    for i in range(len(rowRes)):
        res += ''.join([str(e) for e in rowRes[i]]).replace('-1', '.').replace('0', '.').replace('1', '#') + '\n'
    return res

def cross(S, n):
    res = []
    for i in range(len(S)):
        res.append(S[i][n])
    return tuple(res)

def logicPic(rows, columns):
    N = len(rows)
    M = len(columns)
    unsolvedRows = {x for x in range(N)}
    unsolvedColumns = {x for x in range(M)}
    rowCandidates = {i : frozenset(generate([], rows[i], M)) for i in range(N)}
    columnCandidates = {i : frozenset(generate([], columns[i], N)) for i in range(M)}
    rowRes = {i : tuple([0]*M) for i in range(N)}
    columnRes = {i : tuple([0]*N) for i in range(M)}
    while unsolvedRows != set():
        # look for fields which are the same in every candidate
        for r in unsolvedRows:
            rowRes[r] = orTuple(rowRes[r], andSet(rowCandidates[r]))
        for c in unsolvedColumns:
            columnRes[c] = orTuple(columnRes[c], andSet(columnCandidates[c]))

        # merge solutions on rows and columns
        for r in unsolvedRows:
            rowRes[r] = orTuple(rowRes[r], cross(columnRes, r))
        for c in unsolvedColumns:
            columnRes[c] = orTuple(columnRes[c], cross(rowRes, c))

        # remove candidates which doesnt fit to Result
        for r in unsolvedRows:
            rowCandidates[r] = frozenset({x for x in rowCandidates[r] if andTuple(x, rowRes[r]) == rowRes[r]})
        for c in unsolvedColumns:
            columnCandidates[c] = frozenset({x for x in columnCandidates[c] if andTuple(x, columnRes[c]) == columnRes[c]})

        # set final candidate and remove from unsolved rows/columns
        for r in range(N):
            if len(rowCandidates[r]) == 1:
                rowRes[r] = list(rowCandidates[r])[0]
                unsolvedRows.discard(r)
        for c in range(M):
            if len(columnCandidates[c]) == 1:
                columnRes[c] = list(columnCandidates[c])[0]
                unsolvedColumns.discard(c)
    return boardToString(rowRes)



#######################################################################################################
#
# Main solver
#
#######################################################################################################




def solve():
    test = []
    for line in open('zad_input.txt'):
        test.append([int(x) for x in line.split(" ")])
    # print(test)
    output = logicPic(test[1:1 + test[0][0]], test[1 + test[0][0]:])
    f1 = open('zad_output.txt', 'w+')
    f1.write(output)
    f1.close()
    return

solve()
