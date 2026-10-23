import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Grafo import Grafo
from dibujarGrafo import dibujar_en_canvas
from estilos_tablas import configurar_estilos_tablas
from tabla_pasos import TablaPasosModerna
from estrategias_tablas import RegistroEstrategiasPaso, crear_evento_desde_diccionario
from tabla_cola import TablaColaModerna
from tabla_matriz import TablaMatrizModerna
from ingreso_manual import (
    VentanaIngresoManual,
    ConfiguracionModalManualDTO,
    ResultadoManualDTO,
)

INF = 9999999


class AplicacionGrafo:

    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Camino Minimo")
        self.root.geometry("950x720")
        self.root.configure(bg="#FFFFFF")

        self.grafo_actual = None
        self.nombres_nodos_actuales = []
        self.paso_animacion_actual = 0

        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        configurar_estilos_tablas(self.estilo)
        self.registro_estrategias = RegistroEstrategiasPaso()

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

        self.estilo.configure('Treeview', rowheight=36)

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

        self.frame_canvas_grafo = ttk.Frame(self.frame_grafico)
        self.frame_canvas_grafo.pack(side="top", fill="both", expand=True)

        self.figura = Figure(figsize=(6, 6), facecolor='#FFFFFF')
        self.ax = self.figura.add_subplot(111)
        self.ax.axis('off')

        self.canvas_matplotlib = FigureCanvasTkAgg(self.figura, master=self.frame_canvas_grafo)
        self.canvas_widget = self.canvas_matplotlib.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self.crear_controles_reproduccion()
        self.crear_controles()
        self.crear_estado_vacio()
        self.crear_vista_matriz()

    def crear_controles_reproduccion(self):
        self.frame_reproduccion = ttk.Frame(self.frame_grafico, padding="12 8")

        self.label_explicacion_paso = ttk.Label(
            self.frame_reproduccion,
            text="",
            font=("Helvetica", 10, "bold"),
            foreground="#1E293B",
            anchor="center"
        )
        self.label_explicacion_paso.pack(fill="x", pady=(0, 10))

        self.tabla_cola_prioridad = TablaColaModerna(self.frame_reproduccion)

        frame_botones = ttk.Frame(self.frame_reproduccion)
        frame_botones.pack(anchor="center")

        self.btn_inicio = ttk.Button(
            frame_botones,
            text="⏮ Inicio",
            style='Secundario.TButton',
            command=self.ir_inicio
        )
        self.btn_inicio.pack(side="left", padx=4)

        self.btn_anterior = ttk.Button(
            frame_botones,
            text="◀ Anterior",
            style='Secundario.TButton',
            command=self.ir_paso_anterior
        )
        self.btn_anterior.pack(side="left", padx=4)

        self.btn_siguiente = ttk.Button(
            frame_botones,
            text="Siguiente ▶",
            style='Primario.TButton',
            command=self.ir_paso_siguiente
        )
        self.btn_siguiente.pack(side="left", padx=4)

        self.btn_fin = ttk.Button(
            frame_botones,
            text="Fin ⏭",
            style='Secundario.TButton',
            command=self.ir_fin
        )
        self.btn_fin.pack(side="left", padx=4)

    def mostrar_reproduccion(self):
        self.frame_canvas_grafo.pack_forget()
        self.frame_reproduccion.pack(side="bottom", fill="x", pady=(10, 0))
        self.frame_canvas_grafo.pack(side="top", fill="both", expand=True)

    def ocultar_reproduccion(self):
        if self.frame_reproduccion.winfo_ismapped():
            self.frame_reproduccion.pack_forget()

    def crear_estado_vacio(self):
        self.label_vacio_grafo = ttk.Label(
            self.frame_canvas_grafo,
            text="El grafo visualizado aparecerá aquí",
            font=("Helvetica", 12),
            foreground="#7A7A7A"
        )
        self.label_vacio_grafo.place(relx=0.5, rely=0.5, anchor="center")

    def crear_vista_matriz(self):
        self.frame_opciones_matriz = ttk.Frame(self.frame_matriz)
        self.frame_opciones_matriz.pack(side="top", fill="x", pady=(0, 15))

        ttk.Label(self.frame_opciones_matriz, text="Tipo de Vista:", style='Titulo.TLabel').pack(side="left", padx=(0, 15))

        self.tipo_matriz_var = tk.StringVar(value="pesos")

        ttk.Radiobutton(self.frame_opciones_matriz, text="Matriz de pesos", variable=self.tipo_matriz_var, value="pesos", command=self.actualizar_vista_matriz).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(self.frame_opciones_matriz, text="Matriz de adyacencia", variable=self.tipo_matriz_var, value="directos", command=self.actualizar_vista_matriz).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(self.frame_opciones_matriz, text="Matriz de caminos", variable=self.tipo_matriz_var, value="accesibilidad", command=self.actualizar_vista_matriz).pack(side="left")

        self.tabla_matriz = TablaMatrizModerna(self.frame_matriz)

    def actualizar_vista_matriz(self):
        if self.grafo_actual is None:
            self.tabla_matriz.mostrar_estado_vacio()
            return

        tipo_vista = self.tipo_matriz_var.get()
        matriz = self._obtener_matriz_segun_tipo(tipo_vista)
        self.tabla_matriz.renderizar_matriz(matriz, tipo_vista)

    def _obtener_matriz_segun_tipo(self, tipo_vista):
        if tipo_vista == "pesos":
            return self.grafo_actual.matriz_pesos()
        if tipo_vista == "directos":
            return self.grafo_actual.matriz_adyacencia_binaria()
        return self.grafo_actual.matriz_caminos()

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
        ttk.Radiobutton(frame_radios, text="Manual / Caso Real", variable=self.opcion_generacion, value="manual").pack(side="left")

        self.btn_generar = ttk.Button(self.frame_controles, text="Generar Grafo", style='Secundario.TButton', command=self.evento_generar_grafo)
        self.btn_generar.pack(anchor="w", pady=(0, 30))

        ttk.Label(self.frame_controles, text="Analisis de Ruta", style='Titulo.TLabel').pack(anchor="w", pady=(0, 15))

        frame_rutas = ttk.Frame(self.frame_controles)
        frame_rutas.pack(fill="x", pady=(0, 15))

        # BONO: Combobox desplegables que soportan nombres reales de sedes o índices directos
        frame_inicio = ttk.Frame(frame_rutas)
        frame_inicio.pack(side="left", expand=True, fill="x", padx=(0, 10))
        ttk.Label(frame_inicio, text="Nodo de Inicio:").pack(anchor="w", pady=(0, 5))
        self.entry_inicio = ttk.Combobox(frame_inicio, font=("Helvetica", 10))
        self.entry_inicio.pack(fill="x")

        frame_destino = ttk.Frame(frame_rutas)
        frame_destino.pack(side="left", expand=True, fill="x")
        ttk.Label(frame_destino, text="Nodo de Destino:").pack(anchor="w", pady=(0, 5))
        self.entry_destino = ttk.Combobox(frame_destino, font=("Helvetica", 10))
        self.entry_destino.pack(fill="x")

        self.btn_calcular = ttk.Button(self.frame_controles, text="Calcular Camino Minimo", style='Primario.TButton', command=self.evento_calcular_camino)
        self.btn_calcular.pack(anchor="w", fill="x", pady=(0, 15))

        self.label_resultado = ttk.Label(self.frame_controles, text="", wraplength=320, style='Exito.TLabel')
        self.label_resultado.pack(anchor="w", pady=(0, 20))

        ttk.Label(self.frame_controles, text="Desarrollo Paso a Paso", style='Titulo.TLabel').pack(anchor="w", pady=(0, 10))
        self.frame_texto = ttk.Frame(self.frame_controles)
        self.frame_texto.pack(fill="both", expand=True)

        self.tabla_pasos = TablaPasosModerna(self.frame_texto)

    def evento_generar_grafo(self):
        num_vertices = self._validar_entrada_vertices()
        if num_vertices is None:
            return

        metodo = self.opcion_generacion.get()
        self.ocultar_reproduccion()

        if metodo == "auto":
            self._generar_grafo_automatico(num_vertices)
        elif metodo == "manual":
            self.abrir_ventana_manual(num_vertices)

    def _validar_entrada_vertices(self):
        try:
            num_vertices = int(self.entry_vertices.get())
            if not (5 <= num_vertices <= 15):
                messagebox.showerror("Error", "La cantidad de vertices debe estar entre 5 y 15.")
                return None
            return num_vertices
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un valor numerico entero.")
            return None

    def _generar_grafo_automatico(self, num_vertices):
        self.grafo_actual = Grafo(num_vertices)
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.random() > 0.3:
                    peso = random.randint(1, 50)
                    self.grafo_actual.agregar_arista(i, j, peso)

        nombres_genericos = [f"Nodo {i}" for i in range(num_vertices)]
        self._actualizar_selectores_nodos(nombres_genericos)
        self._refrescar_lienzo_y_tablas("Estado: Grafo generado automaticamente.")

    def abrir_ventana_manual(self, num_vertices):
        config = ConfiguracionModalManualDTO(
            ventana_padre=self.root,
            num_vertices_inicial=num_vertices,
            al_confirmar=self._finalizar_creacion_manual
        )
        VentanaIngresoManual(config)

    def _finalizar_creacion_manual(self, resultado: ResultadoManualDTO):
        self.grafo_actual = resultado.grafo
        # Sincroniza el campo de número de vértices si el archivo JSON tenía otro tamaño
        self.entry_vertices.delete(0, tk.END)
        self.entry_vertices.insert(0, str(self.grafo_actual.V))

        self._actualizar_selectores_nodos(resultado.nombres_nodos)
        self._refrescar_lienzo_y_tablas(f"Estado: {resultado.titulo_caso} cargado.")

    def _actualizar_selectores_nodos(self, nombres_nodos):
        self.nombres_nodos_actuales = list(nombres_nodos)
        opciones = [
            f"{i} - {nombre}" if nombre != f"Nodo {i}" else f"{i}"
            for i, nombre in enumerate(self.nombres_nodos_actuales)
        ]
        self.entry_inicio["values"] = opciones
        self.entry_destino["values"] = opciones
        if opciones:
            self.entry_inicio.set(opciones[0])
            self.entry_destino.set(opciones[-1])

    def _extraer_indice_nodo(self, texto_seleccionado: str) -> int:
        parte_indice = texto_seleccionado.split("-")[0].strip()
        return int(parte_indice)

    def _refrescar_lienzo_y_tablas(self, mensaje_estado: str):
        self.ocultar_reproduccion()
        self.label_resultado.config(text=mensaje_estado, style='Exito.TLabel')
        self.limpiar_paso_a_paso()

        if self.label_vacio_grafo.winfo_ismapped():
            self.label_vacio_grafo.place_forget()

        dibujar_en_canvas(
            self.ax,
            self.canvas_matplotlib,
            self.grafo_actual.aristas,
            self.grafo_actual.V
        )
        self.actualizar_vista_matriz()

    def evento_calcular_camino(self):
        """Orquesta la validación, ejecución algorítmica y renderizado visual (CC = 3)."""
        if self.grafo_actual is None:
            messagebox.showerror("Error", "Primero debe generar un grafo.")
            return

        par_nodos = self._validar_seleccion_nodos()
        if par_nodos is None:
            return  # Guardia temprana: error ya notificado al usuario

        inicio, fin = par_nodos
        self.grafo_actual.camino_minimo(inicio, fin)

        self.paso_animacion_actual = 0
        self.mostrar_reproduccion()
        self._mostrar_resultado_calculo()
        self.renderizar_paso_actual()

    def _mostrar_resultado_calculo(self) -> None:
        if self.grafo_actual.recorrido_minimo == [-1]:
            self.label_resultado.config(
                text="Resultado: No existe un camino posible entre los nodos seleccionados.",
                foreground="#0A0A0A"
            )
            return

        ruta_formateada = self._formatear_ruta_con_nombres(self.grafo_actual.recorrido_minimo)
        texto_exito = f"Ruta: {ruta_formateada}\nCosto Total: {self.grafo_actual.costo_total}"
        self.label_resultado.config(text=texto_exito, style='Exito.TLabel')

    def _validar_seleccion_nodos(self) -> Optional[tuple[int, int]]:
        """Valida que los nodos existan y que inicio != fin (CC = 4)."""
        try:
            inicio = self._extraer_indice_nodo(self.entry_inicio.get())
            fin = self._extraer_indice_nodo(self.entry_destino.get())
        except ValueError:
            messagebox.showerror("Entrada inválida", "Seleccione un nodo de la lista o ingrese un número entero.")
            return None

        num_vertices = self.grafo_actual.V
        if not (0 <= inicio < num_vertices and 0 <= fin < num_vertices):
            messagebox.showerror("Rango inválido", f"Los nodos deben estar entre 0 y {num_vertices - 1}.")
            return None

        if inicio == fin:
            messagebox.showwarning(
                "Nodos idénticos",
                f"El nodo de inicio y destino no pueden ser el mismo (Nodo [{inicio}]).\n"
                "Seleccione dos vértices diferentes para calcular una ruta."
            )
            return None

        return (inicio, fin)

    def _formatear_ruta_con_nombres(self, recorrido):
        if not self.nombres_nodos_actuales:
            return str(recorrido)
        partes = []
        for idx in recorrido:
            nombre = self.nombres_nodos_actuales[idx] if idx < len(self.nombres_nodos_actuales) else f"Nodo {idx}"
            etiqueta = f"[{idx}] {nombre}" if nombre != f"Nodo {idx}" else f"[{idx}]"
            partes.append(etiqueta)
        return " ➔ ".join(partes)

    def limpiar_paso_a_paso(self):
        self.tabla_pasos.limpiar()
        self.tabla_cola_prioridad.mostrar_estado_vacio()
        self.label_explicacion_paso.config(text="")

    def renderizar_paso_actual(self):
        if not self.grafo_actual or not self.grafo_actual.historial_pasos:
            return

        paso_actual = self.grafo_actual.historial_pasos[self.paso_animacion_actual]
        self.label_explicacion_paso.config(text=paso_actual.get('mensaje', ''))

        cola_prioridad = paso_actual.get('cola_prioridad', [])
        self.tabla_cola_prioridad.actualizar_elementos(cola_prioridad)

        filas_a_mostrar = []
        for i in range(self.paso_animacion_actual + 1):
            datos_paso = self.grafo_actual.historial_pasos[i]
            evento = crear_evento_desde_diccionario(i, datos_paso)
            estrategia = self.registro_estrategias.resolver(evento.tipo)
            modelo_fila = estrategia.formatear(evento)
            filas_a_mostrar.append(modelo_fila)

        self.tabla_pasos.renderizar_pasos(filas_a_mostrar)

        nodo_resaltado = None
        arista_resaltada = None
        recorrido_mostrar = []

        if paso_actual['tipo'] == 'Visitado':
            nodo_resaltado = paso_actual.get('nodo')
        elif paso_actual['tipo'] == 'Agregar a cola':
            nodo_resaltado = paso_actual.get('nodo_actual')
            arista_resaltada = (paso_actual.get('nodo_actual'), paso_actual.get('vecino'))
        elif paso_actual['tipo'] == 'Descartado':
            nodo_resaltado = paso_actual.get('nodo_actual')
        elif paso_actual['tipo'] == 'destino_alcanzado':
            nodo_resaltado = paso_actual.get('nodo')

        es_ultimo_paso = (self.paso_animacion_actual == len(self.grafo_actual.historial_pasos) - 1)
        if es_ultimo_paso:
            recorrido_mostrar = self.grafo_actual.recorrido_minimo

        dibujar_en_canvas(
            self.ax,
            self.canvas_matplotlib,
            self.grafo_actual.aristas,
            self.grafo_actual.V,
            recorrido_minimo=recorrido_mostrar,
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