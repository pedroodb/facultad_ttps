from functools import reduce

def movimientos(i,j):
    for movsI in range(0,i):
        yield (movsI,j)
    for movsJ in range(0,j):
        yield (i,movsJ)

def posicionGanadora(i,j,memo):
    if memo[i][j] is None:
        memo[i][j] = reduce(lambda res, sigMov: res or not posicionGanadora(sigMov[0],sigMov[1],memo), movimientos(i,j), False)
    return memo[i][j]

testCases = int(input())
memo = [[None for i in range(3)] for j in range(4)]
for tc in range(testCases):
    n,m = list(map(int,input().split(' ')))
    print('Tuzik' if posicionGanadora((n-1) % 4, (m-1) % 3, memo) else 'Vanya')