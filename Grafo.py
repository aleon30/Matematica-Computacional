from dibujarGrafo import dibujar
import heapq

INF = 9999999

class Grafo:
    def __init__(self, num_vertices):
        self.V = num_vertices
        # Inicializamos la matriz de adyacencia con valores infinitos para los pesos
        self.matriz_adyacencia = [[INF] * num_vertices for _ in range(num_vertices)]
        self.aristas = []
        self.lista_adyacencia = [[] for _ in range(num_vertices)]  # Lista de adyacencia para cada vértice
        self.recorrido_minimo = []

    def agregar_arista(self, vertice1, vertice2, peso):
        # Agregamos la arista a la matriz de adyacencia y a la lista de aristas
        # para el grafo no dirigido
        self.matriz_adyacencia[vertice1][vertice2] = peso
        self.matriz_adyacencia[vertice2][vertice1] = peso

        self.aristas.append((vertice1, vertice2, {'weight': peso}))
        # Se añade la lista de adyacencia para realizar el algoritmo de Dijkstra
        self.lista_adyacencia[vertice1].append((vertice2, peso))
        self.lista_adyacencia[vertice2].append((vertice1, peso))


    def dibujar_grafo(self):
        dibujar(self.aristas, self.recorrido_minimo)
    
    def camino_minimo(self, inicio, fin):
        visitados = [False] * self.V
        distancias = [INF] * self.V
        cola = []
        heapq.heappush(cola, (0, -1, inicio))
        # Algoritmo de Dijkstra
        while len(cola) > 0:
            peso, anterior, actual = heapq.heappop(cola)
            if visitados[actual]:
                continue
            visitados[actual] = True
            distancias[actual] = (peso, anterior, actual)
            if actual == fin:
                break
            for vecino, peso_vecino in self.lista_adyacencia[actual]:
                if not visitados[vecino]:
                    heapq.heappush(cola, (peso + peso_vecino, actual, vecino))
        # Si no hay un camino entre los 2 nodos, se retorna una lista con -1
        if distancias[fin] == INF:
            self.recorrido_minimo = [-1]
            return
        # Reconstruimos el recorrido mínimo desde el nodo de incio hasta el final
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