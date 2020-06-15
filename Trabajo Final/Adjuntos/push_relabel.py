import queue

N = 200
capacities = [[0 for i in range(N)] for j in range(N)]
flow = [[]]
height = []
excess = []
seen = []
overflowed = queue.Queue()


# Capacidad residual de la arista (x,y)
def residual(u ,v):
    return (capacities[u][v] - flow[u][v])

def push(u, v):
    d = min([excess[u], residual(u,v)])
    flow[u][v] += d
    flow[v][u] -= d
    excess[u] -= d
    excess[v] += d
    if (d and excess[v] == d):
        overflowed.put(v)

def relabel(u):
    d = min([height[i] for i in range(N) if residual(u,i) > 0])
    height[u] = d+1

def discharge(u):
    while (excess[u] > 0):
        if (seen[u] < N):
            v = seen[u]
            if (residual(u,v) > 0 and height[u] > height[v]):
                push(u, v)
            else:
                seen[u] += 1
        else:
            relabel(u)
            seen[u] = 0

# Asume que el vertice s esta en la posicion 0 y el vertice t en la posicion N-1
def max_flow():
    global height, flow, excess, seen

    height = [(N if i == 0 else 0) for i in range(N)]
    flow = [[0 for i in range(N)] for j in range(N)]
    excess = [0 for i in range(N)]

    excess[0] = sum(capacities[0])

    for i in range(1,N):
        push(0, i)
    
    seen = [0 for i in range(N)]

    while not overflowed.empty():
        u = overflowed.get()
        if (u != 0 and u != N-1):
            discharge(u)

    return excess[N-1]