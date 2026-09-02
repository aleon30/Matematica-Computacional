import networkx as nx
import matplotlib.pyplot as plt

def dibujar(aristas):
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
    # Dibujamos las etiquetas de las aristas con sus pesos
    nx.draw_networkx_edge_labels(grafo, posicion, edge_labels=texto_aristas)
    # Mostramos el grafo
    plt.show()