import networkx as nx

def dibujar_en_canvas(ax, canvas, aristas, num_vertices, recorrido_minimo=None, nodo_resaltado=None, arista_resaltada=None):
    # Limpiar únicamente los ejes de dibujo sin destruir el widget de la ventana
    ax.clear()
    ax.axis('off')

    # Crear el grafo garantizando que todos los vértices (incluso aislados) existan
    grafo = nx.Graph()
    grafo.add_nodes_from(range(num_vertices))
    grafo.add_edges_from(aristas)
    posicion = nx.circular_layout(grafo)

    # Identificar el color de cada nodo según el paso evaluado
    colores_nodos = ['#FF9800' if nodo == nodo_resaltado else "#249CF1" for nodo in grafo.nodes()]

    # Trazado base de nodos, etiquetas y aristas
    nx.draw_networkx_nodes(grafo, posicion, node_color=colores_nodos, node_size=1200, ax=ax)
    nx.draw_networkx_labels(grafo, posicion, font_color='#FFFFFF', font_weight='bold', font_size=10, ax=ax)
    nx.draw_networkx_edges(grafo, posicion, edge_color='#CBD5E1', width=1.5, ax=ax)

    # Aristas del recorrido mínimo definitivo (en verde)
    aristas_recorrido_minimo = []
    if recorrido_minimo and recorrido_minimo != [-1]:
        for i in range(len(recorrido_minimo) - 1):
            par = tuple(sorted([recorrido_minimo[i], recorrido_minimo[i + 1]]))
            aristas_recorrido_minimo.append(par)

    if aristas_recorrido_minimo:
        nx.draw_networkx_edges(grafo, posicion, edgelist=aristas_recorrido_minimo, width=4, edge_color="#4CAF50", ax=ax)

    # Arista bajo evaluación en el paso actual (en naranja)
    if arista_resaltada:
        u, v = arista_resaltada
        if grafo.has_edge(u, v):
            nx.draw_networkx_edges(grafo, posicion, edgelist=[(u, v)], width=4, edge_color="#FF9800", ax=ax)

    # Pesos de las aristas
    texto_aristas = nx.get_edge_attributes(grafo, 'weight')
    texto_aristas_min = {
        par: peso for par, peso in texto_aristas.items() 
        if tuple(sorted(par)) in aristas_recorrido_minimo
    }

    nx.draw_networkx_edge_labels(grafo, posicion, edge_labels=texto_aristas, font_color='#7A7A7A', ax=ax)
    if texto_aristas_min:
        nx.draw_networkx_edge_labels(grafo, posicion, edge_labels=texto_aristas_min, font_size=11, font_weight='bold', font_color="#4CAF50", ax=ax)

    # Actualizar la vista del lienzo existente
    canvas.draw()