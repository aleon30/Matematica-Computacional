import networkx as nx
import matplotlib.pyplot as plt

def dibujar(aristas, recorrido_minimo):
    fig = plt.figure("Grafo")
    # Inicialización del grafo
    grafo = nx.Graph()
    # Agregamos las aritas al grafo
    grafo.add_edges_from(aristas)
    # Acomodamos la posición de los nodos para una mejor visualización
    posicion = nx.spring_layout(grafo)
    # Dibujamos el grafo con etiquetas y pesos de las aristas
    nx.draw(grafo, 
            posicion, 
            with_labels=True,
            node_color='lightblue',
            node_size=1000)
    # Obtenemos los pesos de las aristas y los dibujamos
    texto_aristas = nx.get_edge_attributes(grafo, 'weight')
    # Cambiamos el color de las aristas que conforman el camino minimo
    aristas_recorrido_minimo = []
    if recorrido_minimo != [-1]:
        for i in range(len(recorrido_minimo)-1):
            aristas_recorrido_minimo.append((recorrido_minimo[i], recorrido_minimo[i+1]))

    nx.draw_networkx_edges(grafo, 
                           posicion, 
                           edgelist=aristas_recorrido_minimo, 
                           width=4,  
                           edge_color="red")
    # Dibujamos las etiquetas de las aristas con sus pesos
    nx.draw_networkx_edge_labels(grafo, posicion, edge_labels=texto_aristas)
    fig.canvas.manager.set_window_title("Grafo y Camino mínimo")
    # Mostramos el grafo
    plt.show()