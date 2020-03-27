from queue import *

def allMovesKing(pos):
    #return possible moves of a king (no other pieces)
    moves = {
        chr(ord(pos[0]) - 1) + chr(ord(pos[1]) - 1),
        chr(ord(pos[0]) - 1) + pos[1],
        chr(ord(pos[0]) - 1) + chr(ord(pos[1]) + 1),
        chr(ord(pos[0]) + 1) + chr(ord(pos[1]) - 1),
        chr(ord(pos[0]) + 1) + pos[1],
        chr(ord(pos[0]) + 1) + chr(ord(pos[1]) + 1),
        pos[0] + chr(ord(pos[1]) - 1),
        pos[0] + chr(ord(pos[1]) + 1)
        }
    return {pos for pos in moves if 'a' <= pos[0] <= 'h' and '1' <= pos[1] <= '8'}

def narrowRooksMoves(minn, maxx, wRook, king, dirr):
    #narrows range of a rook's moves
    if wRook[dirr] == king[dirr] and king[(dirr + 1)%2] < wRook[(dirr + 1)%2]:
        minn = max(minn, king[(dirr + 1)%2])
    if wRook[dirr] == king[dirr] and king[(dirr + 1)%2] > wRook[(dirr + 1)%2]:
        maxx = min(maxx, king[(dirr + 1)%2])
    return minn, maxx

def moveRookNoJumps(wKing, wRook, bKing):
    #return possible moves of a rook but doesn't allow to jump over kings
    minnH, maxxH, minnV, maxxV = 'a', 'i', '1', '9'
    minnV, maxxV = narrowRooksMoves(minnV, maxxV, wRook, wKing, 0)
    minnH, maxxH = narrowRooksMoves(minnH, maxxH, wRook, wKing, 1)
    minnV, maxxV = narrowRooksMoves(minnV, maxxV, wRook, bKing, 0)
    minnH, maxxH = narrowRooksMoves(minnH, maxxH, wRook, bKing, 1)
    horiz = {chr(x) + wRook[1] for x in range(ord(minnH), ord(maxxH))}
    vert = {wRook[0] + chr(x) for x in range(ord(minnV), ord(maxxV))}
    return horiz | vert


def moveRook(wKing, wRook, bKing):
    #return possible moves of a rook (two kings are still on a board)
    forbidden = {wKing, bKing, wRook} | allMovesKing(bKing)
    return moveRookNoJumps(wKing, wRook, bKing) - forbidden


def moveKing(wKing, wRook, bKing, isWhite):
    #return possible moves of a king (other king and a rook are still on a board)
    forbidden = {wKing, bKing, wRook}
    if isWhite:
        return (allMovesKing(wKing) - allMovesKing(bKing)) - forbidden
    else:
        return allMovesKing(bKing) - allMovesKing(wKing) - \
                    moveRookNoJumps(wKing, wRook, bKing) - forbidden


def solve(state, debugMode):
    vis = {state}
    q = Queue()
    q.put([state])
    result = []
    while q.empty() == False:
        ls = q.get()
        #print(ls)
        color, wKing, wRook, bKing = ls[-1].split()
        if color == 'black':
            moves = moveKing(wKing, wRook, bKing, False)
            print(moves)
            input()
            if moves == [] and (wRook[0] == bKing[0] or wRook[1] == bKing[1]) and \
                wKing not in ballMovesKing(bKing) and wRook not in allMovesKing(bKing):
                result = ls
                break
            else:
                for e in moves:
                    q.put(ls + [' '.join(['white', wKing, wRook, e])])
        else:
            for e in moveKing(wKing, wRook, bKing, True):
                newState = ' '.join(['black', e, wRook, bKing])
                if newState not in vis:
                    q.put(ls + [newState])
                    vis.add(newState)
            for e in moveRook(wKing, wRook, bKing):
                newState = ' '.join(['black', wKing, e, bKing])
                if newState not in vis:
                    q.put(ls + [newState])
                    vis.add(newState)
    if debugMode:
        return result
    else:
        return len(result) - 1

print(solve('black c3 a7 a3', True))
#print(sorted(moveKing('d2', 'e3', 'h3', False)))
