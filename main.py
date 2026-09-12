from Grafo import Grafo
import random

# Validación de la dimensión de la matriz
while True:
    try:
        num_vertices = int(input("Ingrese el numero de vértices (entre 5 y 15): "))
        if 5 <= num_vertices <= 15:
            break
        else:
            print("Cantidad no permitida. El valor debe estar comprendido entre 5 y 15.")
    except ValueError:
        print("Entrada inválida. Debe ingresar un valor numérico entero.")

grafo = Grafo(num_vertices)

# Menu de seleccin de metodo
print("\nOpciones para la construcción de la matriz de adyacencia:")
print("1. Generación automatica")
print("2. Ingreso manual")

while True:
    opcion = input("\nSeleccione el método de construcción (1 o 2): ")
    if opcion in ['1', '2']:
        break
    else:
        print("Opción inválida. Seleccione estrictamente 1 o 2.")

# Ejecucion de la opcion seleccionada
if opcion == '1':
    print("\nProcediendo con la generación automática de la matriz...")
    for i in range(num_vertices):
        # Se recorre la mitad superior de la matriz para evitar duplicidad de conexiones
        for j in range(i + 1, num_vertices):
            # Se establece una probabilidad de conexión para evitar la saturación visual del grafo
            if random.random() > 0.3: 
                peso_aleatorio = random.randint(1, 50)
                grafo.agregar_arista(i, j, peso_aleatorio)
    print("Matriz de adyacencia generada satisfactoriamente.")

elif opcion == '2':
    print("\nProcediendo con el ingreso manual.")
    print("Ingrese la magnitud de las conexiones. Indique '0' en caso de no existir conexión directa entre los vértices indicados.")
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            while True:
                try:
                    peso = int(input(f"Magnitud de la conexión entre el vértice {i} y el vértice {j}: "))
                    if peso < 0:
                        print("Restricción matemática incumplida: El valor debe ser no negativo.")
                    else:
                        break
                except ValueError:
                    print("Entrada inválida. Debe ingresar un valor numérico entero.")
            
            if peso > 0:
                grafo.agregar_arista(i, j, peso)

print("\nProyectando la representación visual del grafo ponderado...")
grafo.dibujar_grafo()