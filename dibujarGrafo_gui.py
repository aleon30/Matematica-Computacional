import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dibujar_en_canvas(aristas, recorrido_minimo, frame_destino):
    for widget in frame_destino.winfo_children():
        widget.destroy()
        
    # El fondo de la figura se establece en blanco para combinar con el panel
    fig = plt.figure(figsize=(6, 6), facecolor='#FFFFFF')
    grafo = nx.Graph()
    grafo.add_edges_from(aristas)
    posicion = nx.circular_layout(grafo)
    
    # Dibujar nodos en Azul profundo (#1E3A8A) con texto en Blanco
    # Se aumento un poco el tamano del nodo (1200) para darle mas respiro al texto
    nx.draw(grafo, 
            posicion, 
            with_labels=True,
            node_color='#1E3A8A',
            font_color='#FFFFFF',
            font_weight='bold',
            edge_color='#E2E8F0',
            node_size=1200)
            
    texto_aristas = nx.get_edge_attributes(grafo, 'weight')
    
    aristas_recorrido_minimo = []
    if recorrido_minimo and recorrido_minimo != [-1]:
        for i in range(len(recorrido_minimo)-1):
            par = tuple(sorted([recorrido_minimo[i], recorrido_minimo[i+1]]))
            aristas_recorrido_minimo.append(par)
            
    # Dibujar aristas del recorrido minimo en Verde suave (#4CAF50)
    nx.draw_networkx_edges(grafo, 
                           posicion, 
                           edgelist=aristas_recorrido_minimo, 
                           width=4,  
                           edge_color="#4CAF50")
                           
    texto_aristas_camino_minimo = dict([])
    for arista in aristas:
        par = tuple(sorted([arista[0], arista[1]]))
        if par in aristas_recorrido_minimo:
            peso = arista[2]['weight']
            texto_aristas_camino_minimo[par] = peso
            
    # Etiquetas de aristas estandar en Gris medio
    nx.draw_networkx_edge_labels(grafo, 
                                 posicion, 
                                 edge_labels=texto_aristas,
                                 font_color='#7A7A7A')
    
    # Etiquetas de aristas del camino minimo en Verde suave (#4CAF50)
    nx.draw_networkx_edge_labels(grafo, 
                                posicion, 
                                edge_labels=texto_aristas_camino_minimo,
                                font_size=11,
                                font_weight='bold',
                                font_color="#4CAF50")
                                
    canvas = FigureCanvasTkAgg(fig, master=frame_destino)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    plt.close(fig)