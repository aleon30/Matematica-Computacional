import heapq

INF = 9999999

class Grafo:

    def __init__(self, num_vertices):
        self.V = num_vertices
        self.matriz_adyacencia_ponderada = [[INF] * num_vertices for _ in range(num_vertices)]
        for i in range(num_vertices):
            self.matriz_adyacencia_ponderada[i][i] = 0
        self.aristas = []
        self.lista_adyacencia = [[] for _ in range(num_vertices)]
        self.recorrido_minimo = []
        self.costo_total = 0
        self.historial_pasos = []

    def agregar_arista(self, vertice1, vertice2, peso):
        self.matriz_adyacencia_ponderada[vertice1][vertice2] = peso
        self.matriz_adyacencia_ponderada[vertice2][vertice1] = peso

        self.aristas.append((vertice1, vertice2, {'weight': peso}))
        self.lista_adyacencia[vertice1].append((vertice2, peso))
        self.lista_adyacencia[vertice2].append((vertice1, peso))

    def matriz_pesos(self):
        return self.matriz_adyacencia_ponderada

    def matriz_adyacencia_binaria(self):
        matriz = []
        for i in range(self.V):
            fila = []
            for j in range(self.V):
                if i == j:
                    fila.append(0)
                elif self.matriz_adyacencia_ponderada[i][j] != INF:
                    fila.append(1)
                else:
                    fila.append(0)
            matriz.append(fila)
        return matriz

    def matriz_caminos(self):
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from(self.aristas)
        G.add_nodes_from(range(self.V))
        
        matriz = []
        for i in range(self.V):
            fila = []
            for j in range(self.V):
                if nx.has_path(G, i, j):
                    fila.append(1)
                else:
                    fila.append(0)
            matriz.append(fila)
        return matriz

    def camino_minimo(self, inicio, fin):
        self.costo_total = 0
        self.historial_pasos = []
        visitados = [False] * self.V
        distancias = [INF] * self.V
        
        # Arreglo para registrar los costos mínimos conocidos y realizar la relajación
        mejores_distancias = [INF] * self.V
        mejores_distancias[inicio] = 0
        
        cola = []
        heapq.heappush(cola, (0, -1, inicio))
        
        while len(cola) > 0:
            peso, anterior, actual = heapq.heappop(cola)
            
            if visitados[actual]:
                continue
                
            self.historial_pasos.append({
                'tipo': 'visitando',
                'nodo': actual,
                'costo': peso,
                'mensaje': f"Visitando nodo {actual}. Costo acumulado: {peso}"
            })
            
            visitados[actual] = True
            distancias[actual] = (peso, anterior, actual)
            
            if actual == fin:
                self.costo_total = peso
                self.historial_pasos.append({
                    'tipo': 'destino_alcanzado',
                    'nodo': actual,
                    'mensaje': f"¡Nodo destino {fin} alcanzado!"
                })
                break
                
            for vecino, peso_vecino in self.lista_adyacencia[actual]:
                if not visitados[vecino]:
                    nuevo_peso = peso + peso_vecino
                    costo_conocido = mejores_distancias[vecino]
                    
                    # Proceso de relajación
                    if nuevo_peso < costo_conocido:
                        decision = 'Actualiza'
                        mejores_distancias[vecino] = nuevo_peso
                        heapq.heappush(cola, (nuevo_peso, actual, vecino))
                    else:
                        decision = 'Descarta'
                        
                    self.historial_pasos.append({
                        'tipo': 'evaluando',
                        'nodo_actual': actual,
                        'vecino': vecino,
                        'costo_conocido': costo_conocido,
                        'nuevo_costo': nuevo_peso,
                        'decision': decision,
                        'mensaje': f"Evaluando ruta {actual} -> {vecino}. Conocido: {costo_conocido if costo_conocido != INF else 'INF'}, Nuevo: {nuevo_peso}. {decision}."
                    })
                    
        if distancias[fin] == INF:
            self.recorrido_minimo = [-1]
            return
            
        recorrido = []
        actual = fin
        while actual != inicio:
            recorrido.append(actual)
            for elemento in distancias:
                if elemento == INF:
                    continue
                if elemento[2] == actual:
                    actual = elemento[1]
                    break
        recorrido.append(inicio)
        self.recorrido_minimo = recorrido[::-1]

    