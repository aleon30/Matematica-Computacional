import networkx as nx
import matplotlib.pyplot as plt

def dibujar(aristas, recorrido_minimo):
    fig = plt.figure("Grafo")
    # Inicialización del grafo
    grafo = nx.Graph()
    # Agregamos las aritas al grafo
    grafo.add_edges_from(aristas)
    # Acomodamos la posición de los nodos para una mejor visualización
    posicion = nx.circular_layout(grafo)
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
            par = tuple(sorted([recorrido_minimo[i], recorrido_minimo[i+1]]))
            aristas_recorrido_minimo.append(par)
    # Cambiamos el color de las aristas que conforman el camino mínimo
    nx.draw_networkx_edges(grafo, 
                           posicion, 
                           edgelist=aristas_recorrido_minimo, 
                           width=4,  
                           edge_color="red")
    # Dibujamos las etiquetas de las aristas del camino mínimo con sus pesos
    texto_aristas_camino_minimo = dict([])
    for arista in aristas:
        par = tuple(sorted([arista[0], arista[1]]))
        if par in aristas_recorrido_minimo:
            peso = arista[2]['weight']
            texto_aristas_camino_minimo[par] = peso
    nx.draw_networkx_edge_labels(grafo, 
                                 posicion, 
                                 edge_labels=texto_aristas)
    # Cambiamos el color de las etiquetas con los pesos de las aristas del camino mínimo
    nx.draw_networkx_edge_labels(grafo, 
                                posicion, 
                                edge_labels=texto_aristas_camino_minimo,
                                font_size=10,
                                font_color="red")
    fig.canvas.manager.set_window_title("Grafo y Camino mínimo")
    # Mostramos el grafo
    plt.show()