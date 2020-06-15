#include <bits/stdc++.h>
using namespace std;

// Componentes de la red

int V;
vector<vector<int>> capacities;
vector<vector<int>> adj;

void addEdge(int u, int v, int c) {
  //printf("U:%d V:%d C:%d\n",u,v,c);
  adj[u].push_back(v);
  adj[v].push_back(u);
  capacities[u][v] += c;
}

int findPath(int st, int nd) {
  queue<pair<int, int>> bfs;
  vector<int> parent(V, -1);
  vector<bool> visited(V, false);
  
  bfs.push(make_pair(st, INT_MAX));
  parent[st] = -1;
  visited[st] = true;
  while (!bfs.empty()) {
    pair<int, int> now = bfs.front();
    bfs.pop();
    if (now.first == nd) {
      int ix = now.first;
      while (ix != st) {
        capacities[parent[ix]][ix] -= now.second;
        capacities[ix][parent[ix]] += now.second;
        ix = parent[ix];
      }
      return now.second;
    }
    for (int v : adj[now.first]) {
      if (capacities[now.first][v] > 0) {
        int f = min(capacities[now.first][v], now.second);
        if (!visited[v]) {
          parent[v] = now.first;
          visited[v] = true;
          bfs.push(make_pair(v, f));
        }
      }
    }
  }
  return 0;
}

int maxFlow(int st, int nd) {
  int flow = 0;
  int pathFlow = findPath(st, nd);
  while (pathFlow != 0) {
    flow += pathFlow;
    pathFlow = findPath(st, nd);
  }
  return flow;
}

void findCycle(vector<bool> &inCycle, int N, vector<vector<int>> &adj) {
  stack<pair<int, int>> dfs;
  dfs.push(make_pair(0, INT_MAX));
  vector<int> parent(N, -1);

  while (!dfs.empty()) {
    int u = dfs.top().first;
    int pt = dfs.top().second;
    dfs.pop();
    
    if (parent[u] == -1) {
      parent[u] = pt;
    } else {
      parent[u] = pt;
      int v = u;
      inCycle[v] = true;
      v = parent[v];
      while (u != v) {
        inCycle[v] = true;
        v = parent[v];
      }
      break;
    }

    for (int v : adj[u]) {
      if (v != pt) {
        dfs.push(make_pair(v, u));
      }
    }
  }
}

pair<int,int> getWorkerRoad(int worker, int N, map<int,int> materialToIndex, vector<int> workerList, vector<int> roads) {
  int matIndex = materialToIndex[workerList[worker]];
  for (int i = 0; i < N; ++i) {
    if (capacities[N+2+matIndex][i+2] == 1) {
      capacities[N+2+matIndex][i+2] = 0;
      return make_pair(i+1, roads[i]+1);
    }
  }
  return make_pair(0,0);
}

int main() {

  // Procesando la entrada
  int N, K;
  scanf("%d %d", &N, &K);
  
  // roads: ciudad i construye camino a roadList[i]
  vector<int> roads(N);
  // materialsForRoad: el camino de la ciudad i se puede construir con los materiales de materialsForRoad[i]
  vector<vector<int>> materialsForRoad(N);
  // adjCities: lista de adyacencias en grafo de ciudades y caminos
  vector<vector<int>> adjCities(N);

  for (int i = 0; i < N; ++i) {
    int M;
    scanf("%d %d", &roads[i], &M);
    --roads[i];
    adjCities[i].push_back(roads[i]);
    adjCities[roads[i]].push_back(i);
    materialsForRoad[i].resize(M);
    for (int j = 0; j < M; ++j) {
      scanf("%d", &materialsForRoad[i][j]);
    }
  }

  vector<int> workerList(K);
  // workers: cantidad de trabajadores que manipulan el material i
  vector<int> workers;
  // materialToIndex: Dado un material te da el indice para encontrarlo en workers
  map<int, int> materialToIndex;

  for (int i = 0; i < K; ++i) {
    scanf("%d", &workerList[i]);
    if (materialToIndex.count(workerList[i]) == 0) {
      materialToIndex[workerList[i]] = materialToIndex.size();
      workers.push_back(0);
    }
    ++workers[materialToIndex[workerList[i]]];
  }

  // Encontrar ciclo: cycle[i] es verdadero si la ciudad i pertenece al ciclo

  vector<bool> cycle(N, false);
  findCycle(cycle,N,adjCities);

  // Creacion de la red
  
  // Un vertice por cada ciudad, uno por cada material, un origen (0) y un destino (V-1), y uno extra para limitar el flujo para los nodos del ciclo (1)
  V = (N + 1) + materialToIndex.size() + 2;
  capacities.resize(V, vector<int>(V));
  adj.resize(V);

  int source = 0;
  int extraV = 1;
  int sink = V-1;

  // Conecto el vertice para limitar el flujo, y conecto las ciudades dentro del ciclo a este, mientras que las que esten fuera del ciclo a la fuente
  addEdge(source, extraV, count(cycle.begin(), cycle.end(), true) - 1);
  for (int i = 0; i < N; ++i) {
    if (cycle[i] && cycle[roads[i]]) {
      addEdge(extraV, i+2, 1);
    } else {
      addEdge(source, i+2, 1);
    }
    for (int mat : materialsForRoad[i]) {
      if (materialToIndex.count(mat)) {
        // Conecta el nodo de la ciudad i (i+2) con el de los posibles materiales
        addEdge(i+2, N+2+materialToIndex[mat], 1);
      }
    }
  }

  // Conecta los nodos de los materiales con el destino 
  for (int i = 0; i < materialToIndex.size(); ++i) {
    addEdge(N+2+i, sink, workers[i]);
  }
  
  // Calculo del flujo

  int mf = maxFlow(source, sink);
  
  // Obtencion de camino para cada trabajador

  if (mf < N - 1) {
    printf("-1");
  }
  else {
    for (int i = 0; i < K; ++i) {
      pair<int,int> road = getWorkerRoad(i,N,materialToIndex,workerList,roads);
      printf("%d %d\n",road.first, road.second);
    }
  }

  return 0;
}