import heapq

INF = 9999999

class Grafo:
    def __init__(self, num_vertices):
        self.V = num_vertices
        self.matriz_adyacencia = [[INF] * num_vertices for _ in range(num_vertices)]
        self.aristas = []
        self.lista_adyacencia = [[] for _ in range(num_vertices)]
        self.recorrido_minimo = []
        self.costo_total = 0
        self.historial_pasos = ""

    def agregar_arista(self, vertice1, vertice2, peso):
        self.matriz_adyacencia[vertice1][vertice2] = peso
        self.matriz_adyacencia[vertice2][vertice1] = peso

        self.aristas.append((vertice1, vertice2, {'weight': peso}))
        self.lista_adyacencia[vertice1].append((vertice2, peso))
        self.lista_adyacencia[vertice2].append((vertice1, peso))

    def camino_minimo(self, inicio, fin):
        self.costo_total = 0
        self.historial_pasos = "--- INICIO DEL ALGORITMO DE DIJKSTRA ---\n"
        visitados = [False] * self.V
        distancias = [INF] * self.V
        cola = []
        heapq.heappush(cola, (0, -1, inicio))
        
        while len(cola) > 0:
            peso, anterior, actual = heapq.heappop(cola)
            if visitados[actual]:
                continue
                
            self.historial_pasos += f"-> Visitando nodo {actual} (Costo acumulado: {peso})\n"
            
            visitados[actual] = True
            distancias[actual] = (peso, anterior, actual)
            if actual == fin:
                self.costo_total = peso
                self.historial_pasos += f"¡Nodo destino {fin} alcanzado!\n"
                break
                
            for vecino, peso_vecino in self.lista_adyacencia[actual]:
                if not visitados[vecino]:
                    nuevo_peso = peso + peso_vecino
                    self.historial_pasos += f"   Evaluando vecino {vecino} | Nuevo costo posible: {nuevo_peso}\n"
                    heapq.heappush(cola, (nuevo_peso, actual, vecino))
                    
        self.historial_pasos += "----------------------------------------\n"
        
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