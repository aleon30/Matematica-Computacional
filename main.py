from Grafo import Grafo

# Pedimos el numero de vertices hasta que sea una cantidad permitida
while True:
    num_vertices = int(input("Ingrese el número de vértices (entre 5 y 15): "))
    
    if 5 <= num_vertices <= 15:
        break  # Si el número es correcto, se sale de la repeticion
    else:
        print("Cantidad no permitida. Por favor, ingrese un valor entre 5 y 15.")

grafo = Grafo(num_vertices)

aristas = int(input("Ingrese el número de aristas: "))

print("Ingrese las aristas en el formato: vertice1 vertice2 peso")

for i in range(aristas):
    print(f"Arista {i + 1}: ", end="")
    # Los vértices y el peso se ingresan como enteros separados por espacios
    vertice1, vertice2, peso = map(int, input().split())
    grafo.agregar_arista(vertice1, vertice2, peso)

grafo.dibujar_grafo()