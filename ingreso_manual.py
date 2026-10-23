import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass
from typing import Callable, Optional, Sequence
from Grafo import Grafo
from estilos_tablas import (
    COLOR_FONDO_BASE,
    COLOR_GRIS_100,
    COLOR_GRIS_200,
    COLOR_GRIS_300,
    COLOR_GRIS_400,
    COLOR_GRIS_500,
    COLOR_GRIS_700,
    COLOR_GRIS_800,
    COLOR_PRIMARIO_100,
    COLOR_PRIMARIO_900,
    COLOR_EXITO_FONDO,
    COLOR_EXITO_TEXTO,
    COLOR_PELIGRO_FONDO,
    COLOR_PELIGRO_TEXTO,
    FUENTE_CABECERA,
    FUENTE_CELDA,
)


@dataclass(frozen=True)
class CoordenadaCeldaDTO:
    """Representa una coordenada (fila, columna) dentro de la matriz."""
    fila: int
    columna: int


@dataclass(frozen=True)
class AristaManualDTO:
    """Representa una arista ponderada validada."""
    origen: int
    destino: int
    peso: int


@dataclass(frozen=True)
class ResultadoManualDTO:
    """DTO emitido al confirmar la creación manual o carga de caso de estudio."""
    grafo: Grafo
    nombres_nodos: Sequence[str]
    titulo_caso: str


@dataclass(frozen=True)
class ConfiguracionModalManualDTO:
    """Agrupa los parámetros de entrada del modal (cumple regla <= 3 parámetros)."""
    ventana_padre: tk.Widget
    num_vertices_inicial: int
    al_confirmar: Callable[[ResultadoManualDTO], None]


class MatrizManualModel:
    """
    Encapsula el estado de la cuadrícula manual, garantizando diagonal en 0,
    simetría automática (i, j) == (j, i), nombres de sedes y validación de pesos.
    """

    def __init__(self, num_vertices: int) -> None:
        self.reiniciar_dimension(num_vertices)

    def reiniciar_dimension(self, num_vertices: int) -> None:
        self.num_vertices = num_vertices
        self.titulo_caso = "Grafo configurado manualmente"
        self.nombres_nodos: list[str] = [f"Nodo {i}" for i in range(num_vertices)]
        self._pesos: list[list[int]] = [
            [0 for _ in range(num_vertices)] for _ in range(num_vertices)
        ]

    # Modificador (Command): valida y asigna simétricamente el peso (CC = 4)
    def intentar_asignar_peso(self, coord: CoordenadaCeldaDTO, texto: str) -> bool:
        if coord.fila == coord.columna:
            return True

        texto_limpio = texto.strip()
        if self._es_entrada_vacia_o_cero(texto_limpio):
            self._establecer_par_simetrico(coord, 0)
            return True

        peso = self._convertir_a_entero_positivo(texto_limpio)
        if peso is None:
            self._establecer_par_simetrico(coord, 0)
            return False

        self._establecer_par_simetrico(coord, peso)
        return True

    def limpiar_todo(self) -> None:
        self.titulo_caso = "Grafo configurado manualmente"
        self.nombres_nodos = [f"Nodo {i}" for i in range(self.num_vertices)]
        for i in range(self.num_vertices):
            self._pesos[i] = [0] * self.num_vertices

    def cargar_plantilla_demostracion(self) -> None:
        self.limpiar_todo()
        self.titulo_caso = "Plantilla de prueba conexa"
        for i in range(self.num_vertices - 1):
            peso_base = ((i * 7 + 5) % 25) + 4
            self._establecer_par_simetrico(CoordenadaCeldaDTO(i, i + 1), peso_base)

            if i + 2 < self.num_vertices:
                peso_cruzado = ((i * 11 + 9) % 30) + 8
                self._establecer_par_simetrico(CoordenadaCeldaDTO(i, i + 2), peso_cruzado)

    def cargar_desde_diccionario(self, datos: dict) -> Optional[str]:
        n_archivo = datos.get("cantidadVertices")
        if not isinstance(n_archivo, int) or not (5 <= n_archivo <= 15):
            return "El campo 'cantidadVertices' debe ser un entero entre 5 y 15."

        self.reiniciar_dimension(n_archivo)
        self.titulo_caso = str(datos.get("empresa", "Caso de Estudio Empresarial"))
        self._cargar_nombres_personalizados(datos.get("nombresNodos", []))
        return self._cargar_conexiones_json(datos.get("conexiones", []))

    def obtener_peso(self, coord: CoordenadaCeldaDTO) -> int:
        return self._pesos[coord.fila][coord.columna]

    def exportar_aristas(self) -> Sequence[AristaManualDTO]:
        aristas: list[AristaManualDTO] = []
        for i in range(self.num_vertices):
            self._recolectar_aristas_de_fila(i, aristas)
        return aristas

    def construir_resultado(self) -> ResultadoManualDTO:
        nuevo_grafo = Grafo(self.num_vertices)
        for arista in self.exportar_aristas():
            nuevo_grafo.agregar_arista(arista.origen, arista.destino, arista.peso)

        return ResultadoManualDTO(
            grafo=nuevo_grafo,
            nombres_nodos=tuple(self.nombres_nodos),
            titulo_caso=self.titulo_caso
        )

    # Métodos privados auxiliares (CC <= 4)
    def _es_entrada_vacia_o_cero(self, texto: str) -> bool:
        if texto in ("", "∞"):
            return True
        return texto.isdigit() and int(texto) == 0

    def _cargar_nombres_personalizados(self, lista_nombres: list) -> None:
        if not isinstance(lista_nombres, list):
            return
        for i in range(min(len(lista_nombres), self.num_vertices)):
            self.nombres_nodos[i] = str(lista_nombres[i])

    def _cargar_conexiones_json(self, conexiones: list) -> Optional[str]:
        if not isinstance(conexiones, list):
            return "El formato de 'conexiones' debe ser una lista."

        for item in conexiones:
            if not self._procesar_item_conexion(item):
                return "Existen conexiones con nodos fuera de rango o pesos inválidos."
        return None

    def _procesar_item_conexion(self, item: dict) -> bool:
        u = item.get("origen")
        v = item.get("destino")
        peso = item.get("peso")
        if not all(isinstance(x, int) for x in (u, v, peso)):
            return False
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            return False
        return self.intentar_asignar_peso(CoordenadaCeldaDTO(u, v), str(peso))

    def _recolectar_aristas_de_fila(self, fila: int, acumulador: list[AristaManualDTO]) -> None:
        for col in range(fila + 1, self.num_vertices):
            peso = self._pesos[fila][col]
            if peso > 0:
                acumulador.append(AristaManualDTO(fila, col, peso))

    def _establecer_par_simetrico(self, coord: CoordenadaCeldaDTO, peso: int) -> None:
        self._pesos[coord.fila][coord.columna] = peso
        self._pesos[coord.columna][coord.fila] = peso

    def _convertir_a_entero_positivo(self, texto: str) -> Optional[int]:
        if not texto.isdigit():
            return None
        valor = int(texto)
        return valor if valor > 0 else None


# 3. Adaptador de Interfaz: Ventana Modal con Scrollbars y Pie Anclado

class VentanaIngresoManual(tk.Toplevel):
    """
    Ventana modal con cuadrícula n x n desplazable (soporta hasta 15x15 sin cortar botones),
    bloqueo de diagonal principal, reflejo simétrico en vivo y lector de casos (.json).
    """

    def __init__(self, config: ConfiguracionModalManualDTO) -> None:
        super().__init__(config.ventana_padre)
        self._config = config
        self._modelo = MatrizManualModel(config.num_vertices_inicial)
        self._celdas_ui: dict[tuple[int, int], tk.Entry] = {}
        self._celdas_con_error: set[tuple[int, int]] = set()
        self._sincronizando: bool = False

        self._configurar_ventana()
        self._construir_interfaz()

    def _configurar_ventana(self) -> None:
        self.title("Ingreso Manual y Caso de Estudio — Matriz Simétrica")
        self.geometry("880x580")
        self.minsize(680, 440)
        self.configure(bg=COLOR_FONDO_BASE)
        self.resizable(True, True)
        self.transient(self._config.ventana_padre)
        self.grab_set()

    def _construir_interfaz(self) -> None:
        self._marco_principal = ttk.Frame(self, padding="24 16 24 16")
        self._marco_principal.pack(fill=tk.BOTH, expand=True)

        # 1. Encabezado y barra superior fijos arriba
        self._construir_encabezado(self._marco_principal)
        self._construir_barra_herramientas(self._marco_principal)

        # 2. IMPORTANTE: Empaquetar el pie con side=BOTTOM ANTES del contenedor expandible
        # para garantizar que el botón "Guardar" nunca sea empujado fuera de la ventana.
        self._construir_pie_acciones(self._marco_principal)

        # 3. Contenedor central desplazable (ocupa el espacio restante)
        self._construir_area_desplazable(self._marco_principal)
        self._reconstruir_cuadricula_visual()
        self._actualizar_resumen_estado()

    def _construir_encabezado(self, padre: ttk.Frame) -> None:
        ttk.Label(
            padre,
            text="Configuración Manual de la Matriz de Pesos",
            style="Titulo.TLabel"
        ).pack(side=tk.TOP, anchor=tk.W, pady=(0, 4))

        self._lbl_subtitulo = ttk.Label(
            padre,
            text="",
            style="Secundario.TLabel"
        )
        self._lbl_subtitulo.pack(side=tk.TOP, anchor=tk.W, pady=(0, 12))
        self._actualizar_texto_subtitulo()

    def _actualizar_texto_subtitulo(self) -> None:
        n = self._modelo.num_vertices
        self._lbl_subtitulo.config(
            text=(
                f"Caso activo: {self._modelo.titulo_caso} ({n}×{n} nodos). "
                "La matriz aplica simetría automática en espejo y fija la diagonal en 0."
            )
        )

    def _construir_barra_herramientas(self, padre: ttk.Frame) -> None:
        barra = ttk.Frame(padre)
        barra.pack(side=tk.TOP, fill=tk.X, pady=(0, 12))

        self._etiqueta_estado = tk.Label(
            barra,
            text="● 0 aristas configuradas",
            font=FUENTE_CABECERA,
            bg=COLOR_PRIMARIO_100,
            fg=COLOR_PRIMARIO_900,
            padx=12,
            pady=4
        )
        self._etiqueta_estado.pack(side=tk.LEFT)

        ttk.Button(
            barra,
            text="Limpiar celdas",
            style="Secundario.TButton",
            command=self._evento_limpiar_matriz
        ).pack(side=tk.RIGHT, padx=(8, 0))

        ttk.Button(
            barra,
            text="⚡ Plantilla rápida",
            style="Secundario.TButton",
            command=self._evento_cargar_plantilla
        ).pack(side=tk.RIGHT, padx=(8, 0))

        ttk.Button(
            barra,
            text="📂 Cargar Caso (.json)",
            style="Secundario.TButton",
            command=self._evento_cargar_archivo_json
        ).pack(side=tk.RIGHT)

    def _construir_pie_acciones(self, padre: ttk.Frame) -> None:
        pie = ttk.Frame(padre)
        pie.pack(side=tk.BOTTOM, fill=tk.X, pady=(12, 0))

        ttk.Label(
            pie,
            text="Nota: Las celdas vacías indican ausencia de conexión directa (∞).",
            style="Secundario.TLabel"
        ).pack(side=tk.LEFT)

        ttk.Button(
            pie,
            text="Guardar grafo y visualizar",
            style="Primario.TButton",
            command=self._evento_confirmar_y_guardar
        ).pack(side=tk.RIGHT)

    def _construir_area_desplazable(self, padre: ttk.Frame) -> None:
        marco_scroll = tk.Frame(
            padre,
            bg=COLOR_GRIS_100,
            highlightbackground=COLOR_GRIS_200,
            highlightthickness=1
        )
        marco_scroll.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._scroll_y = ttk.Scrollbar(marco_scroll, orient=tk.VERTICAL)
        self._scroll_x = ttk.Scrollbar(marco_scroll, orient=tk.HORIZONTAL)

        self._canvas_matriz = tk.Canvas(
            marco_scroll,
            bg=COLOR_GRIS_100,
            highlightthickness=0,
            yscrollcommand=self._scroll_y.set,
            xscrollcommand=self._scroll_x.set
        )

        self._scroll_y.config(command=self._canvas_matriz.yview)
        self._scroll_x.config(command=self._canvas_matriz.xview)

        self._scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self._scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._canvas_matriz.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._interior_matriz = tk.Frame(self._canvas_matriz, bg=COLOR_GRIS_100, padx=14, pady=14)
        self._canvas_matriz.create_window((0, 0), window=self._interior_matriz, anchor="nw")

        self._interior_matriz.bind(
            "<Configure>",
            lambda _e: self._canvas_matriz.configure(scrollregion=self._canvas_matriz.bbox("all"))
        )
        self._vincular_rueda_raton()

    def _vincular_rueda_raton(self) -> None:
        self.bind("<MouseWheel>", self._al_girar_rueda)

    def _al_girar_rueda(self, evento: tk.Event) -> None:
        pasos = int(-1 * (evento.delta / 120))
        self._canvas_matriz.yview_scroll(pasos, "units")

    def _reconstruir_cuadricula_visual(self) -> None:
        for widget in self._interior_matriz.winfo_children():
            widget.destroy()

        self._celdas_ui.clear()
        self._celdas_con_error.clear()

        self._renderizar_cabeceras_columnas(self._interior_matriz)
        for fila in range(self._modelo.num_vertices):
            self._renderizar_fila_matriz(self._interior_matriz, fila)

        self._interior_matriz.update_idletasks()
        self._canvas_matriz.configure(scrollregion=self._canvas_matriz.bbox("all"))
        self._canvas_matriz.yview_moveto(0.0)
        self._canvas_matriz.xview_moveto(0.0)

    def _renderizar_cabeceras_columnas(self, contenedor: tk.Frame) -> None:
        tk.Label(
            contenedor,
            text="ORIGEN \\ DEST",
            font=FUENTE_CABECERA,
            bg=COLOR_GRIS_100,
            fg=COLOR_GRIS_500,
            width=14,
            anchor="e"
        ).grid(row=0, column=0, padx=4, pady=(0, 6))

        for col in range(self._modelo.num_vertices):
            tk.Label(
                contenedor,
                text=f"[{col}]",
                font=FUENTE_CABECERA,
                bg=COLOR_GRIS_100,
                fg=COLOR_GRIS_700,
                width=5
            ).grid(row=0, column=col + 1, padx=2, pady=(0, 6))

    def _renderizar_fila_matriz(self, contenedor: tk.Frame, fila: int) -> None:
        nombre_corto = self._modelo.nombres_nodos[fila][:12]
        etiqueta_fila = f"[{fila}] {nombre_corto}" if nombre_corto != f"Nodo {fila}" else f"Nodo [{fila}]"

        tk.Label(
            contenedor,
            text=etiqueta_fila,
            font=FUENTE_CABECERA,
            bg=COLOR_GRIS_100,
            fg=COLOR_GRIS_700,
            width=14,
            anchor="e"
        ).grid(row=fila + 1, column=0, padx=(0, 8), pady=2)

        for col in range(self._modelo.num_vertices):
            self._crear_celda_individual(contenedor, CoordenadaCeldaDTO(fila, col))

    def _crear_celda_individual(self, contenedor: tk.Frame, coord: CoordenadaCeldaDTO) -> None:
        if coord.fila == coord.columna:
            self._crear_celda_diagonal_bloqueada(contenedor, coord)
            return

        celda = tk.Entry(
            contenedor,
            width=5,
            justify="right",
            font=FUENTE_CELDA,
            bg=COLOR_FONDO_BASE,
            fg=COLOR_GRIS_800,
            relief="flat",
            highlightbackground=COLOR_GRIS_300,
            highlightcolor=COLOR_PRIMARIO_900,
            highlightthickness=1
        )
        celda.grid(row=coord.fila + 1, column=coord.columna + 1, padx=2, pady=2, ipady=3)
        celda.bind("<KeyRelease>", lambda _e, c=coord: self._al_editar_celda(c))
        self._celdas_ui[(coord.fila, coord.columna)] = celda

    def _crear_celda_diagonal_bloqueada(self, contenedor: tk.Frame, coord: CoordenadaCeldaDTO) -> None:
        celda_fija = tk.Label(
            contenedor,
            text="0",
            width=5,
            anchor="e",
            padx=4,
            font=FUENTE_CELDA,
            bg=COLOR_GRIS_200,
            fg=COLOR_GRIS_400
        )
        celda_fija.grid(row=coord.fila + 1, column=coord.columna + 1, padx=2, pady=2, ipady=3)

    # -------------------------------------------------------------------------
    # Manejadores de Eventos con Guardia Antirretorno (CC <= 4)
    # -------------------------------------------------------------------------

    def _al_editar_celda(self, coord: CoordenadaCeldaDTO) -> None:
        if self._sincronizando:
            return

        celda_origen = self._celdas_ui[(coord.fila, coord.columna)]
        es_valido = self._modelo.intentar_asignar_peso(coord, celda_origen.get())

        if not es_valido:
            self._marcar_estado_celda(coord, tiene_error=True)
            self._reflejar_en_celda_espejo(coord)
            self._actualizar_resumen_estado()
            return

        self._marcar_estado_celda(coord, tiene_error=False)
        self._reflejar_en_celda_espejo(coord)
        self._actualizar_resumen_estado()

    def _reflejar_en_celda_espejo(self, coord: CoordenadaCeldaDTO) -> None:
        coord_espejo = CoordenadaCeldaDTO(coord.columna, coord.fila)
        celda_espejo = self._celdas_ui[(coord_espejo.fila, coord_espejo.columna)]
        peso = self._modelo.obtener_peso(coord)
        texto_espejo = str(peso) if peso > 0 else ""

        self._sincronizando = True
        celda_espejo.delete(0, tk.END)
        celda_espejo.insert(0, texto_espejo)
        self._marcar_estado_celda(coord_espejo, tiene_error=False)
        self._sincronizando = False

    def _marcar_estado_celda(self, coord: CoordenadaCeldaDTO, tiene_error: bool) -> None:
        llave = (coord.fila, coord.columna)
        celda = self._celdas_ui[llave]

        if tiene_error:
            self._celdas_con_error.add(llave)
            celda.configure(bg=COLOR_PELIGRO_FONDO, fg=COLOR_PELIGRO_TEXTO, highlightbackground=COLOR_PELIGRO_TEXTO)
            return

        self._celdas_con_error.discard(llave)
        celda.configure(bg=COLOR_FONDO_BASE, fg=COLOR_GRIS_800, highlightbackground=COLOR_GRIS_300)

    def _actualizar_resumen_estado(self) -> None:
        if self._celdas_con_error:
            self._etiqueta_estado.configure(
                text="✕ Error: Ingrese solo enteros positivos",
                bg=COLOR_PELIGRO_FONDO,
                fg=COLOR_PELIGRO_TEXTO
            )
            return

        total_aristas = len(self._modelo.exportar_aristas())
        if total_aristas == 0:
            self._etiqueta_estado.configure(
                text="● 0 aristas configuradas",
                bg=COLOR_PRIMARIO_100,
                fg=COLOR_PRIMARIO_900
            )
            return

        self._etiqueta_estado.configure(
            text=f"✓ {total_aristas} aristas activas ({self._modelo.titulo_caso})",
            bg=COLOR_EXITO_FONDO,
            fg=COLOR_EXITO_TEXTO
        )

    def _evento_cargar_archivo_json(self) -> None:
        ruta = filedialog.askopenfilename(
            parent=self,
            title="Seleccionar archivo de Caso de Estudio (.json)",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return

        datos = self._leer_json_seguro(ruta)
        if datos is None:
            return

        mensaje_error = self._modelo.cargar_desde_diccionario(datos)
        if mensaje_error:
            messagebox.showerror("Archivo inválido", mensaje_error, parent=self)
            return

        self._actualizar_texto_subtitulo()
        self._reconstruir_cuadricula_visual()
        self._sincronizar_vista_desde_modelo()

    def _leer_json_seguro(self, ruta: str) -> Optional[dict]:
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception as err:
            messagebox.showerror("Error de lectura", f"No se pudo leer el JSON:\n{err}", parent=self)
            return None

    def _evento_cargar_plantilla(self) -> None:
        self._modelo.cargar_plantilla_demostracion()
        self._actualizar_texto_subtitulo()
        self._reconstruir_cuadricula_visual()
        self._sincronizar_vista_desde_modelo()

    def _evento_limpiar_matriz(self) -> None:
        self._modelo.limpiar_todo()
        self._actualizar_texto_subtitulo()
        self._reconstruir_cuadricula_visual()
        self._sincronizar_vista_desde_modelo()

    def _sincronizar_vista_desde_modelo(self) -> None:
        self._sincronizando = True
        self._celdas_con_error.clear()

        for (fila, col), celda in self._celdas_ui.items():
            peso = self._modelo.obtener_peso(CoordenadaCeldaDTO(fila, col))
            celda.delete(0, tk.END)
            if peso > 0:
                celda.insert(0, str(peso))
            celda.configure(bg=COLOR_FONDO_BASE, fg=COLOR_GRIS_800, highlightbackground=COLOR_GRIS_300)

        self._sincronizando = False
        self._actualizar_resumen_estado()

    def _evento_confirmar_y_guardar(self) -> None:
        if self._celdas_con_error:
            messagebox.showerror(
                "Valores inválidos",
                "Corrija las celdas marcadas en rojo antes de guardar.",
                parent=self
            )
            return

        if not self._modelo.exportar_aristas():
            messagebox.showwarning(
                "Grafo vacío",
                "Configure al menos una conexión antes de guardar.",
                parent=self
            )
            return

        resultado = self._modelo.construir_resultado()
        self.destroy()
        self._config.al_confirmar(resultado)