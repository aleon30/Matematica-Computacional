import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from Grafo import Grafo
from dibujarGrafo import dibujar_en_canvas

class AplicacionGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Camino Minimo")
        self.root.geometry("950x700")
        self.root.configure(bg="#FFFFFF")
        
        self.grafo_actual = None
        self.paso_animacion_actual = 0  # Inicialización de la variable de estado
        
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        
        self.estilo.configure('TFrame', background='#FFFFFF')
        
        FUENTE_BASE = ("Helvetica", 10)
        FUENTE_TITULO = ("Helvetica", 14, "bold")
        FUENTE_SECUNDARIA = ("Helvetica", 9)
        
        COLOR_PRIMARIO = "#1E3A8A"
        COLOR_TEXTO = "#0A0A0A"
        COLOR_SECUNDARIO = "#7A7A7A"
        COLOR_EXITO = "#4CAF50"
        COLOR_FONDO = "#FFFFFF"
        
        self.estilo.configure('TLabel', background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_BASE)
        self.estilo.configure('Titulo.TLabel', background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_TITULO)
        self.estilo.configure('Secundario.TLabel', background=COLOR_FONDO, foreground=COLOR_SECUNDARIO, font=FUENTE_SECUNDARIA)
        self.estilo.configure('Exito.TLabel', background=COLOR_FONDO, foreground=COLOR_EXITO, font=("Helvetica", 10, "bold"))
        
        self.estilo.configure('Primario.TButton', background=COLOR_PRIMARIO, foreground=COLOR_FONDO, font=("Helvetica", 10, "bold"), borderwidth=0, padding=8)
        self.estilo.map('Primario.TButton', background=[('active', '#2C3E50')])
        
        self.estilo.configure('Secundario.TButton', background="#E2E8F0", foreground=COLOR_TEXTO, font=("Helvetica", 10), borderwidth=0, padding=8)
        self.estilo.map('Secundario.TButton', background=[('active', '#CBD5E1')])
        
        self.estilo.configure('TRadiobutton', background=COLOR_FONDO, foreground=COLOR_TEXTO, font=FUENTE_BASE)
        self.estilo.map('TRadiobutton', background=[('active', COLOR_FONDO)])
        
        self.estilo.configure('TNotebook', background=COLOR_FONDO, borderwidth=0)
        self.estilo.configure('TNotebook.Tab', background="#E2E8F0", foreground=COLOR_TEXTO, padding=[10, 5], font=FUENTE_BASE)
        self.estilo.map('TNotebook.Tab', background=[('selected', COLOR_PRIMARIO)], foreground=[('selected', COLOR_FONDO)])
        
        self.panel_principal = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=COLOR_FONDO, borderwidth=0)
        self.panel_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.frame_controles = ttk.Frame(self.panel_principal, padding="20 10 30 10")
        self.panel_principal.add(self.frame_controles, minsize=380, stretch="never")
        
        self.notebook_central = ttk.Notebook(self.panel_principal)
        self.panel_principal.add(self.notebook_central, minsize=500, stretch="always")
        
        self.frame_grafico = ttk.Frame(self.notebook_central, padding="10")
        self.notebook_central.add(self.frame_grafico, text="Grafo Visual")
        
        self.frame_matriz = ttk.Frame(self.notebook_central, padding="10")
        self.notebook_central.add(self.frame_matriz, text="Representación matricial")
        
        # Creación de controles de reproducción (permanecen ocultos en la inicialización)
        self.crear_controles_reproduccion()
        
        # Sub-contenedor exclusivo para el canvas para evitar que eliminar widgets afecte a los botones
        self.frame_canvas_grafo = ttk.Frame(self.frame_grafico)
        self.frame_canvas_grafo.pack(side="top", fill="both", expand=True)
        
        self.crear_controles()
        self.crear_estado_vacio()
        self.crear_vista_matriz()

    def crear_controles_reproduccion(self):
        self.frame_reproduccion = ttk.Frame(self.frame_grafico)
        
        self.label_explicacion_paso = ttk.Label(self.frame_reproduccion, text="", font=("Helvetica", 11, "italic"), anchor="center")
        self.label_explicacion_paso.pack(fill="x", pady=(0, 10))
        
        frame_botones = ttk.Frame(self.frame_reproduccion)
        frame_botones.pack(anchor="center")
        
        self.btn_inicio = ttk.Button(frame_botones, text="[<<] Inicio", style='Secundario.TButton', command=self.ir_inicio)
        self.btn_inicio.pack(side="left", padx=5)
        
        self.btn_anterior = ttk.Button(frame_botones, text="[<] Anterior", style='Secundario.TButton', command=self.ir_paso_anterior)
        self.btn_anterior.pack(side="left", padx=5)
        
        self.btn_siguiente = ttk.Button(frame_botones, text="[>] Siguiente", style='Secundario.TButton', command=self.ir_paso_siguiente)
        self.btn_siguiente.pack(side="left", padx=5)
        
        self.btn_fin = ttk.Button(frame_botones, text="[>>] Fin", style='Secundario.TButton', command=self.ir_fin)
        self.btn_fin.pack(side="left", padx=5)

    def mostrar_reproduccion(self):
        self.frame_canvas_grafo.pack_forget()
        self.frame_reproduccion.pack(side="bottom", fill="x", pady=(10, 0))
        self.frame_canvas_grafo.pack(side="top", fill="both", expand=True)

    def ocultar_reproduccion(self):
        if self.frame_reproduccion.winfo_ismapped():
            self.frame_reproduccion.pack_forget()

    def crear_estado_vacio(self):
        # El texto vacío ahora se vincula al sub-contenedor del canvas
        self.label_vacio_grafo = ttk.Label(self.frame_canvas_grafo, text="El grafo visualizado aparecera aqui", font=("Helvetica", 12), foreground="#7A7A7A")
        self.label_vacio_grafo.place(relx=0.5, rely=0.5, anchor="center")

    def crear_vista_matriz(self):
        self.frame_opciones_matriz = ttk.Frame(self.frame_matriz)
        
        ttk.Label(self.frame_opciones_matriz, text="Tipo de Vista:", style='Titulo.TLabel').pack(side="left", padx=(0, 15))
        
        self.tipo_matriz_var = tk.StringVar(value="pesos")
        
        ttk.Radiobutton(self.frame_opciones_matriz, text="Matriz de pesos", variable=self.tipo_matriz_var, value="pesos", command=self.actualizar_vista_matriz).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(self.frame_opciones_matriz, text="Matriz de adyacencia", variable=self.tipo_matriz_var, value="directos", command=self.actualizar_vista_matriz).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(self.frame_opciones_matriz, text="Matriz de caminos", variable=self.tipo_matriz_var, value="accesibilidad", command=self.actualizar_vista_matriz).pack(side="left")

        self.label_vacio_matriz = ttk.Label(self.frame_matriz, text="Genere un grafo para visualizar la matriz de adyacencia", font=("Helvetica", 12), foreground="#7A7A7A")
        self.label_vacio_matriz.place(relx=0.5, rely=0.5, anchor="center")
        
        self.frame_tree = ttk.Frame(self.frame_matriz)
        self.scroll_y_matriz = ttk.Scrollbar(self.frame_tree, orient="vertical")
        self.scroll_y_matriz.pack(side="right", fill="y")
        self.scroll_x_matriz = ttk.Scrollbar(self.frame_tree, orient="horizontal")
        self.scroll_x_matriz.pack(side="bottom", fill="x")
        self.tree_matriz = ttk.Treeview(self.frame_tree, show="headings", yscrollcommand=self.scroll_y_matriz.set, xscrollcommand=self.scroll_x_matriz.set)
        self.scroll_y_matriz.config(command=self.tree_matriz.yview)
        self.scroll_x_matriz.config(command=self.tree_matriz.xview)
        self.tree_matriz.pack(side="left", fill="both", expand=True)

    def actualizar_vista_matriz(self):
        if self.grafo_actual is None:
            return
            
        if self.label_vacio_matriz.winfo_exists():
            self.label_vacio_matriz.place_forget()
            
        self.frame_opciones_matriz.pack(side="top", fill="x", pady=(0, 10))
        self.frame_tree.pack(fill="both", expand=True)
        
        for item in self.tree_matriz.get_children():
            self.tree_matriz.delete(item)
            
        n = self.grafo_actual.V
        columnas = ["Origen"] + [f"Destino {i}" for i in range(n)]
        self.tree_matriz["columns"] = columnas
        self.tree_matriz.heading("Origen", text="Origen \\ Destino")
        self.tree_matriz.column("Origen", width=120, anchor="center", stretch=False)
        
        for i in range(n):
            col_name = f"Destino {i}"
            self.tree_matriz.heading(col_name, text=str(i))
            self.tree_matriz.column(col_name, width=65, anchor="center", stretch=True)
            
        tipo_vista = self.tipo_matriz_var.get()
        
        if tipo_vista == "pesos":
            matriz = self.grafo_actual.matriz_pesos()
        elif tipo_vista == "directos":
            matriz = self.grafo_actual.matriz_caminos_directos()
        else:
            matriz = self.grafo_actual.matriz_accesibilidad()

        for i in range(n):
            fila = [f"{i}"]
            for j in range(n):
                valor = matriz[i][j]
                if tipo_vista == "pesos":
                    if valor == 9999999:
                        fila.append("∞") 
                    else:
                        fila.append(str(valor))
                else:
                    fila.append(str(valor))
            self.tree_matriz.insert("", "end", values=fila)

    def crear_controles(self):
        ttk.Label(self.frame_controles, text="Configuracion del Grafo", style='Titulo.TLabel').pack(anchor="w", pady=(0, 15))
        
        frame_vertices = ttk.Frame(self.frame_controles)
        frame_vertices.pack(fill="x", pady=(0, 15))
        ttk.Label(frame_vertices, text="Numero de vertices:").pack(side="left")
        ttk.Label(frame_vertices, text="(5 al 15)", style='Secundario.TLabel').pack(side="left", padx=(5, 10))
        self.entry_vertices = ttk.Entry(frame_vertices, width=8, font=("Helvetica", 10))
        self.entry_vertices.pack(side="left")
        
        ttk.Label(self.frame_controles, text="Metodo de generacion:").pack(anchor="w", pady=(5, 5))
        frame_radios = ttk.Frame(self.frame_controles)
        frame_radios.pack(fill="x", pady=(0, 15))
        self.opcion_generacion = tk.StringVar(value="auto")
        ttk.Radiobutton(frame_radios, text="Automatica", variable=self.opcion_generacion, value="auto").pack(side="left", padx=(0, 15))
        ttk.Radiobutton(frame_radios, text="Manual", variable=self.opcion_generacion, value="manual").pack(side="left")
        
        self.btn_generar = ttk.Button(self.frame_controles, text="Generar Grafo", style='Secundario.TButton', command=self.evento_generar_grafo)
        self.btn_generar.pack(anchor="w", pady=(0, 30))
        
        ttk.Label(self.frame_controles, text="Analisis de Ruta", style='Titulo.TLabel').pack(anchor="w", pady=(0, 15))
        
        frame_rutas = ttk.Frame(self.frame_controles)
        frame_rutas.pack(fill="x", pady=(0, 15))
        
        frame_inicio = ttk.Frame(frame_rutas)
        frame_inicio.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ttk.Label(frame_inicio, text="Nodo de Inicio:").pack(anchor="w", pady=(0, 5))
        self.entry_inicio = ttk.Entry(frame_inicio, font=("Helvetica", 10))
        self.entry_inicio.pack(fill="x")
        
        frame_destino = ttk.Frame(frame_rutas)
        frame_destino.pack(side="left", expand=True, fill="x")
        ttk.Label(frame_destino, text="Nodo de Destino:").pack(anchor="w", pady=(0, 5))
        self.entry_destino = ttk.Entry(frame_destino, font=("Helvetica", 10))
        self.entry_destino.pack(fill="x")
        
        self.btn_calcular = ttk.Button(self.frame_controles, text="Calcular Camino Minimo", style='Primario.TButton', command=self.evento_calcular_camino)
        self.btn_calcular.pack(anchor="w", fill="x", pady=(0, 15))
        
        self.label_resultado = ttk.Label(self.frame_controles, text="", wraplength=320, style='Exito.TLabel')
        self.label_resultado.pack(anchor="w", pady=(0, 20))
        
        ttk.Label(self.frame_controles, text="Desarrollo Paso a Paso", style='Titulo.TLabel').pack(anchor="w", pady=(0, 10))
        self.frame_texto = ttk.Frame(self.frame_controles)
        self.frame_texto.pack(fill="both", expand=True)
        
        self.scroll_texto = ttk.Scrollbar(self.frame_texto)
        self.scroll_texto.pack(side="right", fill="y")
        
        columnas = ("Paso", "Nodo", "Vecino", "Cálculo", "Decisión")
        self.tabla_pasos = ttk.Treeview(self.frame_texto, columns=columnas, show="headings", yscrollcommand=self.scroll_texto.set, height=8)
        self.tabla_pasos.pack(side="left", fill="both", expand=True)
        self.scroll_texto.config(command=self.tabla_pasos.yview)
        
        self.tabla_pasos.heading("Paso", text="Paso")
        self.tabla_pasos.column("Paso", width=40, anchor="center")
        
        self.tabla_pasos.heading("Nodo", text="Nodo")
        self.tabla_pasos.column("Nodo", width=50, anchor="center")
        
        self.tabla_pasos.heading("Vecino", text="Vecino")
        self.tabla_pasos.column("Vecino", width=50, anchor="center")
        
        self.tabla_pasos.heading("Cálculo", text="Cálculo")
        self.tabla_pasos.column("Cálculo", width=120, anchor="center")
        
        self.tabla_pasos.heading("Decisión", text="Decisión")
        self.tabla_pasos.column("Decisión", width=90, anchor="center")
        
        self.tabla_pasos.tag_configure('actualiza', foreground='#15803D')
        self.tabla_pasos.tag_configure('descarta', foreground='#94A3B8')
        self.tabla_pasos.tag_configure('visita', foreground='#1E3A8A', font=('Helvetica', 9, 'bold'))

    def evento_generar_grafo(self):
        try:
            num_vertices = int(self.entry_vertices.get())
            if not (5 <= num_vertices <= 15):
                messagebox.showerror("Error", "La cantidad de vertices debe estar entre 5 y 15.")
                return
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un valor numerico entero.")
            return
            
        self.grafo_actual = Grafo(num_vertices)
        metodo = self.opcion_generacion.get()
        
        self.ocultar_reproduccion()
        
        if metodo == "auto":
            for i in range(num_vertices):
                for j in range(i + 1, num_vertices):
                    if random.random() > 0.3: 
                        peso = random.randint(1, 50)
                        self.grafo_actual.agregar_arista(i, j, peso)
                        
            self.label_resultado.config(text="Estado: Grafo generado automaticamente.", style='Exito.TLabel')
            self.limpiar_paso_a_paso()
            # Ahora la gráfica se inserta sobre el frame_canvas_grafo
            dibujar_en_canvas(self.grafo_actual.aristas, [], self.frame_canvas_grafo)
            self.actualizar_vista_matriz()
            
        elif metodo == "manual":
            self.abrir_ventana_manual(num_vertices)

    def abrir_ventana_manual(self, num_vertices):
        ventana_manual = tk.Toplevel(self.root)
        ventana_manual.title("Ingreso Manual")
        ventana_manual.geometry("400x360")
        ventana_manual.configure(bg="#FFFFFF")
        
        frame_interior = ttk.Frame(ventana_manual, padding="20")
        frame_interior.pack(fill="both", expand=True)

        ttk.Label(frame_interior, text="Agregar aristas al grafo", style='Titulo.TLabel').pack(pady=(0, 15))

        frame_entradas = ttk.Frame(frame_interior)
        frame_entradas.pack(fill="x", pady=(0, 15))

        ttk.Label(frame_entradas, text="Vértice 1").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(frame_entradas, text="Vértice 2").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(frame_entradas, text="Peso").grid(row=0, column=2, padx=5, pady=5)

        entrada_vertice1 = ttk.Entry(frame_entradas, width=9, font=("Helvetica", 10))
        entrada_vertice1.grid(row=1, column=0, padx=5)
        entrada_vertice2 = ttk.Entry(frame_entradas, width=9, font=("Helvetica", 10))
        entrada_vertice2.grid(row=1, column=1, padx=5)
        entrada_peso = ttk.Entry(frame_entradas, width=9, font=("Helvetica", 10))
        entrada_peso.grid(row=1, column=2, padx=5)

        etiqueta_estado = ttk.Label(frame_interior, text=f"Vértices válidos: 0 a {num_vertices - 1}", style='Secundario.TLabel')
        etiqueta_estado.pack(pady=(0, 10))

        def agregar_arista_manual():
            try:
                vertice1 = int(entrada_vertice1.get())
                vertice2 = int(entrada_vertice2.get())
                peso = int(entrada_peso.get())
            except ValueError:
                messagebox.showerror("Error", "Ingrese valores enteros para ambos vértices y el peso.", parent=ventana_manual)
                return

            if not (0 <= vertice1 < num_vertices) or not (0 <= vertice2 < num_vertices):
                messagebox.showerror("Error", f"Los vértices deben estar en el rango 0 a {num_vertices - 1}.", parent=ventana_manual)
                return
            if vertice1 == vertice2:
                messagebox.showerror("Error", "Una arista debe conectar dos vértices distintos.", parent=ventana_manual)
                return
            if peso <= 0:
                messagebox.showerror("Error", "El peso debe ser un entero positivo.", parent=ventana_manual)
                return
            if self.grafo_actual.matriz_adyacencia[vertice1][vertice2] != 9999999:
                messagebox.showerror("Error", "Ya existe una arista entre esos vértices.", parent=ventana_manual)
                return

            self.grafo_actual.agregar_arista(vertice1, vertice2, peso)
            etiqueta_estado.config(text=f"Arista agregada: {vertice1} - {vertice2} (peso {peso}).")
            entrada_vertice1.delete(0, tk.END)
            entrada_vertice2.delete(0, tk.END)
            entrada_peso.delete(0, tk.END)
            entrada_vertice1.focus_set()

        def guardar_grafo():
            self.ocultar_reproduccion()
            ventana_manual.destroy()
            self.label_resultado.config(text="Estado: Grafo manual generado exitosamente.", style='Exito.TLabel')
            self.limpiar_paso_a_paso()
            dibujar_en_canvas(self.grafo_actual.aristas, [], self.frame_canvas_grafo)
            self.actualizar_vista_matriz()

        ttk.Button(frame_interior, text="Añadir arista", style='Secundario.TButton', command=agregar_arista_manual).pack(pady=(0, 10))
        ttk.Button(frame_interior, text="Guardar grafo y visualizar", style='Primario.TButton', command=guardar_grafo).pack(pady=10)

    def evento_calcular_camino(self):
        if self.grafo_actual is None:
            messagebox.showerror("Error", "Primero debe generar un grafo.")
            return
            
        try:
            inicio = int(self.entry_inicio.get())
            fin = int(self.entry_destino.get())
            num_vertices = self.grafo_actual.V 
            
            if not (0 <= inicio < num_vertices) or not (0 <= fin < num_vertices):
                messagebox.showerror("Error", f"Los nodos ingresados no existen. Rango valido: 0 a {num_vertices-1}.")
                return
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar valores enteros para los nodos.")
            return
            
        self.grafo_actual.camino_minimo(inicio, fin)
        
        # Reiniciar el contador al inicio y desplegar la botonera de reproducción
        self.paso_animacion_actual = 0
        self.mostrar_reproduccion()
        
        if self.grafo_actual.recorrido_minimo == [-1]:
            texto_res = "Resultado: No existe un camino posible."
            self.label_resultado.config(text=texto_res, foreground="#0A0A0A")
        else:
            texto_res = f"Ruta: {self.grafo_actual.recorrido_minimo}\nCosto Total: {self.grafo_actual.costo_total}"
            self.label_resultado.config(text=texto_res, style='Exito.TLabel')
            
        # Se renderiza el fotograma inicial en el gráfico y en la tabla de pasos
        self.renderizar_paso_actual()

    def limpiar_paso_a_paso(self):
        self.tabla_pasos.delete(*self.tabla_pasos.get_children())

    def renderizar_paso_actual(self):
        if not self.grafo_actual or not self.grafo_actual.historial_pasos:
            return
            
        paso_actual = self.grafo_actual.historial_pasos[self.paso_animacion_actual]
        self.label_explicacion_paso.config(text=paso_actual.get('mensaje', ''))
        
        # Limpiar la tabla antes de rellenar el historial hasta el fotograma actual
        self.limpiar_paso_a_paso()
        
        ultima_fila = None
        
        # Iterar e insertar filas desde el paso 0 hasta el paso_animacion_actual
        for i in range(self.paso_animacion_actual + 1):
            p = self.grafo_actual.historial_pasos[i]
            
            if p['tipo'] == 'visitando':
                valores = (i, p['nodo'], "-", f"Costo: {p['costo']}", "Visitando")
                ultima_fila = self.tabla_pasos.insert("", "end", values=valores, tags=('visita',))
                
            elif p['tipo'] == 'evaluando':
                # Preparar el texto de cálculo comparando el nuevo costo vs el ya conocido
                costo_conocido = p.get('costo_conocido', 'INF')
                if costo_conocido == 9999999:
                    costo_conocido = "INF"
                    
                calculo_str = f"Nuevo: {p['nuevo_costo']} (vs {costo_conocido})"
                decision = p['decision']
                
                tag = 'actualiza' if decision == 'Actualiza' else 'descarta'
                valores = (i, p['nodo_actual'], p['vecino'], calculo_str, decision)
                ultima_fila = self.tabla_pasos.insert("", "end", values=valores, tags=(tag,))
                
            elif p['tipo'] == 'destino_alcanzado':
                valores = (i, p['nodo'], "-", "-", "Destino!")
                ultima_fila = self.tabla_pasos.insert("", "end", values=valores, tags=('visita',))
                
        # Hacer scroll automático a la última fila insertada
        if ultima_fila:
            self.tabla_pasos.see(ultima_fila)
            
        # Renderizado visual del grafo para el fotograma actual
        nodo_resaltado = None
        arista_resaltada = None
        recorrido_mostrar = []
        
        if paso_actual['tipo'] == 'visitando':
            nodo_resaltado = paso_actual.get('nodo')
        elif paso_actual['tipo'] == 'evaluando':
            nodo_resaltado = paso_actual.get('nodo_actual')
            arista_resaltada = (paso_actual.get('nodo_actual'), paso_actual.get('vecino'))
        elif paso_actual['tipo'] == 'destino_alcanzado':
            nodo_resaltado = paso_actual.get('nodo')
            
        es_ultimo_paso = (self.paso_animacion_actual == len(self.grafo_actual.historial_pasos) - 1)
        if es_ultimo_paso:
            recorrido_mostrar = self.grafo_actual.recorrido_minimo
            
        dibujar_en_canvas(
            self.grafo_actual.aristas, 
            recorrido_mostrar, 
            self.frame_canvas_grafo, 
            nodo_resaltado=nodo_resaltado, 
            arista_resaltada=arista_resaltada
        )

    def ir_paso_siguiente(self):
        if not self.grafo_actual or not self.grafo_actual.historial_pasos:
            return
        if self.paso_animacion_actual < len(self.grafo_actual.historial_pasos) - 1:
            self.paso_animacion_actual += 1
            self.renderizar_paso_actual()

    def ir_paso_anterior(self):
        if not self.grafo_actual or not self.grafo_actual.historial_pasos:
            return
        if self.paso_animacion_actual > 0:
            self.paso_animacion_actual -= 1
            self.renderizar_paso_actual()

    def ir_inicio(self):
        if not self.grafo_actual or not self.grafo_actual.historial_pasos:
            return
        self.paso_animacion_actual = 0
        self.renderizar_paso_actual()

    def ir_fin(self):
        if not self.grafo_actual or not self.grafo_actual.historial_pasos:
            return
        self.paso_animacion_actual = len(self.grafo_actual.historial_pasos) - 1
        self.renderizar_paso_actual()

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGrafo(root)
    root.mainloop()