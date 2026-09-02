from dibujarGrafo import dibujar

INF = 9999999

class Grafo:
    def __init__(self, num_vertices):
        self.V = num_vertices
        # Inicializamos la matriz de adyacencia con valores infinitos para los pesos
        self.matriz_adjacencia = [[INF] * num_vertices for _ in range(num_vertices)]
        self.aristas = []

    def agregar_arista(self, vertice1, vertice2, peso):
        # Agregamos la arista a la matriz de adyacencia y a la lista de aristas
        # para el grafo no dirigido
        self.matriz_adjacencia[vertice1][vertice2] = peso
        self.matriz_adjacencia[vertice2][vertice1] = peso
        self.aristas.append((vertice1, vertice2, {'weight': peso}))

    def dibujar_grafo(self):
        dibujar(self.aristas)