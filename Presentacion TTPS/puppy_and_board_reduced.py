from functools import reduce

def movimientos(i,j):
    for movsI in range(0,i):
        yield (movsI,j)
    for movsJ in range(0,j):
        yield (i,movsJ)

def posicionGanadora(i,j):
    return reduce(lambda res, sigMov: res or not posicionGanadora(sigMov[0],sigMov[1]), movimientos(i,j), False)

testCases = int(input())
for tc in range(testCases):
    n,m = list(map(int,input().split(' ')))
    print('Tuzik' if posicionGanadora((n-1) % 4, (m-1) % 3) else 'Vanya')