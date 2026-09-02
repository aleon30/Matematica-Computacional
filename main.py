from Grafo import Grafo

num_vertices = int(input("Ingrese el número de vértices: "))

grafo = Grafo(num_vertices)

aristas = int(input("Ingrese el número de aristas: "))

print("Ingrese las aristas en el formato: vertice1 vertice2 peso")

for i in range(aristas):
    print(f"Arista {i + 1}: ", end="")
    # Los vértices y el peso se ingresan como enteros separados por espacios
    vertice1, vertice2, peso = map(int, input().split())
    grafo.agregar_arista(vertice1, vertice2, peso)

grafo.dibujar_grafo()