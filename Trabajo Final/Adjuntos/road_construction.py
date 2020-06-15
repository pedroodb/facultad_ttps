import queue
import sys

def findPath(s, t):
    q = queue.Queue()
    prev = [-1 for i in range(V)]
    visited = [False for i in range(V)]

    q.put((s, None))
    visited[s] = True

    while(not q.empty()):
        node, cap = q.get()
        if (node == t):
            while (node != s):
                capacities[prev[node]][node] -= cap
                capacities[node][prev[node]] += cap
                node = prev[node]
            return cap
        for each in adj[node]:
            if capacities[node][each] > 0:
                if not visited[each]:
                    prev[each] = node
                    visited[each] = True
                    minCap = capacities[node][each] if (
                        cap == None) else min([cap, capacities[node][each]])
                    q.put((each, minCap))

    return 0

def maxFlow(s, t):
    flow = 0
    pathCapacity = findPath(s, t)
    while pathCapacity != 0:
        flow += pathCapacity
        pathCapacity = findPath(s, t)
    return flow

def addEdge(i, j,n):
    #print('U:',i,'V:',j,'N:',n)
    adj[i].append(j)
    adj[j].append(i)
    capacities[i][j] = n
    capacities[j][i] = 0


def getWorkerRoad(worker):
    matIndex = materialToIndex[workerList[worker]]
    for i in range(N):
        if capacities[N+2+matIndex][i+2] == 1:
            capacities[N+2+matIndex][i+2] = 0
            return(i+1, roads[i]+1)
    return(0, 0)

def findCycle(adj):
    inCycle = [False for i in range(N)]
    dfs = []
    dfs.append((0, None))
    prev = [-1 for i in range(N)]

    while (dfs):
        node, previous = dfs.pop()

        if (prev[node] == -1):
            prev[node] = previous
        else:
            prev[node] = previous
            v = node

            inCycle[v] = True
            v = prev[v]
            while (node != v):
                inCycle[v] = True
                v = prev[v]
            break

        for v in adj[node]:
            if (v != previous):
                dfs.append((v, node))

    return inCycle

# Procesando la entrada

N, K = map(int, sys.stdin.readline().split(' '))

# roads: ciudad i construye camino a roadList[i]
roads = []
# materialsForRoad: el camino de la ciudad i se puede construir con los materiales de materialsForRoad[i]
materialsForRoad = [[] for i in range(N)]
# adjCities: lista de adjacencias en grafo de ciudades y caminos
adjCities = [[] for i in range(N)]

for i in range(N):
    inp = list(map(int, sys.stdin.readline().split(' ')))

    destination = inp[0]-1
    
    roads.append(destination)
    adjCities[i].append(destination)
    adjCities[destination].append(i)

    materialsForRoad[i] = inp[2:]

workerList = list(map(int, sys.stdin.readline().split(' ')))
# workers: cantidad de trabajadores que manipulan el material i
workers = []
# materialToIndex: Dado un material te da el indice para encontrarlo en workers
materialToIndex = {}

for worker, material in enumerate(workerList):
    if material not in materialToIndex:
        materialToIndex[material] = len(materialToIndex)
        workers.append(0)

    workers[materialToIndex[material]] += 1

# Encontrar ciclo: cycle[i] es verdadero si la ciudad i pertenece al ciclo
cycle = findCycle(adjCities)

# Creacion de la red

# Un vertice por cada ciudad, uno por cada material, un origen (0) y un destino (V-1), y uno extra para limitar el flujo para los nodos del ciclo (1)
V = N + len(materialToIndex) + 3
capacities = [[-1 for i in range(V)] for j in range(V)]
adj = [[] for i in range(V)]

# Conecto el vertice para limitar el flujo, y conecto las ciudades dentro del ciclo a este, mientras que las que esten fuera del ciclo a la fuente
addEdge(0, 1,cycle.count(True)-1)
for i in range(N):
    if cycle[i] and cycle[roads[i]]:
        addEdge(1, i+2,1)
    else:
        addEdge(0, i+2,1)
    for material in materialsForRoad[i]:
        if material in materialToIndex:
            addEdge(i+2, N+2+materialToIndex[material], 1)

for i in range(len(materialToIndex)):
    addEdge(N+2+i, V-1, workers[i])

# Calculo del flujo
flow = maxFlow(0, V-1)
if (flow < N - 1):
    print(-1)
else:
    for worker in range(K):
        a, b = getWorkerRoad(worker)
        sys.stdout.write(str(a)+' '+str(b)+'\n')
