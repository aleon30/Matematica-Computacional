import tkinter as tk
from tkinter import ttk, messagebox
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
    """Identifica una posición (fila, columna) dentro de la cuadrícula."""
    fila: int
    columna: int


@dataclass(frozen=True)
class AristaManualDTO:
    """Representa una conexión ponderada válida lista para inyectar en Grafo."""
    origen: int
    destino: int
    peso: int


@dataclass(frozen=True)
class ConfiguracionModalManualDTO:
    """Agrupa las dependencias de entrada del modal (cumple regla <= 3 parámetros)."""
    ventana_padre: tk.Widget
    grafo_destino: Grafo
    al_confirmar: Callable[[], None]




class MatrizManualModel:
    """
    Encapsula el estado de la cuadrícula manual, garantizando diagonal en 0,
    simetría automática (i, j) == (j, i) y validación de pesos enteros positivos.
    """

    def __init__(self, num_vertices: int) -> None:
        self.num_vertices = num_vertices
        self._pesos: list[list[int]] = [
            [0 for _ in range(num_vertices)] for _ in range(num_vertices)
        ]

    # Modificador (Command): valida y asigna simétricamente el peso (CC = 4)
    def intentar_asignar_peso(self, coord: CoordenadaCeldaDTO, texto: str) -> bool:
        if coord.fila == coord.columna:
            return True

        texto_limpio = texto.strip()
        if texto_limpio in ("", "0", "∞"):
            self._establecer_par_simetrico(coord, 0)
            return True

        peso = self._convertir_a_entero_positivo(texto_limpio)
        if peso is None:
            return False

        self._establecer_par_simetrico(coord, peso)
        return True

    # Modificador (Command): limpia todas las conexiones a cero (CC = 2)
    def limpiar_todo(self) -> None:
        for i in range(self.num_vertices):
            self._pesos[i] = [0] * self.num_vertices

    # Modificador (Command): pre-carga una red conexa editable para demostración (CC = 3)
    def cargar_plantilla_demostracion(self) -> None:
        self.limpiar_todo()
        for i in range(self.num_vertices - 1):
            peso_base = ((i * 7 + 5) % 25) + 4
            self._establecer_par_simetrico(CoordenadaCeldaDTO(i, i + 1), peso_base)

            if i + 2 < self.num_vertices:
                peso_cruzado = ((i * 11 + 9) % 30) + 8
                self._establecer_par_simetrico(CoordenadaCeldaDTO(i, i + 2), peso_cruzado)

    # Consulta pura (Query): devuelve el valor actual de una celda (CC = 1)
    def obtener_peso(self, coord: CoordenadaCeldaDTO) -> int:
        return self._pesos[coord.fila][coord.columna]

    # Consulta pura (Query): exporta las aristas del triángulo superior (CC = 3)
    def exportar_aristas(self) -> Sequence[AristaManualDTO]:
        aristas: list[AristaManualDTO] = []
        for i in range(self.num_vertices):
            self._recolectar_aristas_de_fila(i, aristas)
        return aristas

    # Métodos privados de ocultamiento de información (CC <= 3)
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



# 3. Adaptador de Interfaz: Módulo Profundo de Cuadrícula Manual

class VentanaIngresoManual(tk.Toplevel):
    """
    Ventana modal con cuadrícula n x n interactiva, bloqueo de diagonal principal,
    reflejo simétrico automático en vivo y jerarquía de botones Refactoring UI.
    """

    def __init__(self, config: ConfiguracionModalManualDTO) -> None:
        super().__init__(config.ventana_padre)
        self._config = config
        self._modelo = MatrizManualModel(config.grafo_destino.V)
        self._celdas_ui: dict[tuple[int, int], tk.Entry] = {}
        self._celdas_con_error: set[tuple[int, int]] = set()
        self._sincronizando: bool = False

        self._configurar_ventana()
        self._construir_interfaz()

    # Configuración base de ventana modal (CC = 1)
    def _configurar_ventana(self) -> None:
        self.title("Ingreso Manual — Matriz de Adyacencia Ponderada")
        self.configure(bg=COLOR_FONDO_BASE)
        self.resizable(True, True)
        self.transient(self._config.ventana_padre)
        self.grab_set()

    # Orquestación visual en bloques según escala de espaciado (CC = 1)
    def _construir_interfaz(self) -> None:
        marco_principal = ttk.Frame(self, padding="24 20 24 20")
        marco_principal.pack(fill=tk.BOTH, expand=True)

        self._construir_encabezado(marco_principal)
        self._construir_barra_herramientas(marco_principal)
        self._construir_cuadricula_simetrica(marco_principal)
        self._construir_pie_acciones(marco_principal)
        self._actualizar_resumen_estado()

    def _construir_encabezado(self, padre: ttk.Frame) -> None:
        ttk.Label(
            padre,
            text="Configuración Manual de Pesos",
            style="Titulo.TLabel"
        ).pack(anchor=tk.W, pady=(0, 4))

        subtitulo = (
            f"Ingrese los costos entre nodos (0 a {self._modelo.num_vertices - 1}). "
            "La matriz aplica simetría automática en espejo y bloquea la diagonal en 0."
        )
        ttk.Label(
            padre,
            text=subtitulo,
            style="Secundario.TLabel"
        ).pack(anchor=tk.W, pady=(0, 16))

    def _construir_barra_herramientas(self, padre: ttk.Frame) -> None:
        barra = ttk.Frame(padre)
        barra.pack(fill=tk.X, pady=(0, 12))

        # Indicador de estado en vivo (combina texto e icono para accesibilidad WCAG)
        self._etiqueta_estado = tk.Label(
            barra,
            text="● 0 aristas activas",
            font=FUENTE_CABECERA,
            bg=COLOR_PRIMARIO_100,
            fg=COLOR_PRIMARIO_900,
            padx=12,
            pady=4
        )
        self._etiqueta_estado.pack(side=tk.LEFT)

        # Acciones secundarias (menor prominencia visual que el botón primario)
        ttk.Button(
            barra,
            text="Limpiar celdas",
            style="Secundario.TButton",
            command=self._evento_limpiar_matriz
        ).pack(side=tk.RIGHT, padx=(8, 0))

        ttk.Button(
            barra,
            text="⚡ Cargar plantilla conexa",
            style="Secundario.TButton",
            command=self._evento_cargar_plantilla
        ).pack(side=tk.RIGHT)

    def _construir_cuadricula_simetrica(self, padre: ttk.Frame) -> None:
        # Contenedor con fondo gris frío sutil (gray-100) en lugar de bordes ruidosos
        contenedor_tabla = tk.Frame(
            padre,
            bg=COLOR_GRIS_100,
            padx=16,
            pady=16,
            highlightbackground=COLOR_GRIS_200,
            highlightthickness=1
        )
        contenedor_tabla.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self._renderizar_cabeceras_columnas(contenedor_tabla)
        for fila in range(self._modelo.num_vertices):
            self._renderizar_fila_matriz(contenedor_tabla, fila)

    def _renderizar_cabeceras_columnas(self, contenedor: tk.Frame) -> None:
        tk.Label(
            contenedor,
            text="NODO",
            font=FUENTE_CABECERA,
            bg=COLOR_GRIS_100,
            fg=COLOR_GRIS_500,
            width=6
        ).grid(row=0, column=0, padx=4, pady=(0, 8))

        for col in range(self._modelo.num_vertices):
            tk.Label(
                contenedor,
                text=f"[{col}]",
                font=FUENTE_CABECERA,
                bg=COLOR_GRIS_100,
                fg=COLOR_GRIS_700,
                width=5
            ).grid(row=0, column=col + 1, padx=3, pady=(0, 8))

    def _renderizar_fila_matriz(self, contenedor: tk.Frame, fila: int) -> None:
        tk.Label(
            contenedor,
            text=f"[{fila}]",
            font=FUENTE_CABECERA,
            bg=COLOR_GRIS_100,
            fg=COLOR_GRIS_700,
            width=6,
            anchor="e"
        ).grid(row=fila + 1, column=0, padx=(0, 8), pady=3)

        for col in range(self._modelo.num_vertices):
            self._crear_celda_individual(contenedor, CoordenadaCeldaDTO(fila, col))

    def _crear_celda_individual(self, contenedor: tk.Frame, coord: CoordenadaCeldaDTO) -> None:
        if coord.fila == coord.columna:
            self._crear_celda_diagonal_bloqueada(contenedor, coord)
            return

        celda = tk.Entry(
            contenedor,
            width=5,
            justify="right",  # Regla innegociable: números alineados a la derecha
            font=FUENTE_CELDA,
            bg=COLOR_FONDO_BASE,
            fg=COLOR_GRIS_800,
            relief="flat",
            highlightbackground=COLOR_GRIS_300,
            highlightcolor=COLOR_PRIMARIO_900,
            highlightthickness=1
        )
        celda.grid(row=coord.fila + 1, column=coord.columna + 1, padx=3, pady=3, ipady=4)
        celda.bind(
            "<KeyRelease>",
            lambda _e, c=coord: self._al_editar_celda(c)
        )
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
        celda_fija.grid(row=coord.fila + 1, column=coord.columna + 1, padx=3, pady=3, ipady=4)

    def _construir_pie_acciones(self, padre: ttk.Frame) -> None:
        pie = ttk.Frame(padre)
        pie.pack(fill=tk.X)

        ttk.Label(
            pie,
            text="Nota: Las celdas vacías representan ausencia de conexión directa (∞).",
            style="Secundario.TLabel"
        ).pack(side=tk.LEFT)

        # Único botón Primario en toda la vista (Jerarquía de acciones Refactoring UI)
        ttk.Button(
            pie,
            text="Guardar grafo y visualizar",
            style="Primario.TButton",
            command=self._evento_confirmar_y_guardar
        ).pack(side=tk.RIGHT)



    def _al_editar_celda(self, coord: CoordenadaCeldaDTO) -> None:
        if self._sincronizando:
            return

        celda_origen = self._celdas_ui[(coord.fila, coord.columna)]
        texto_actual = celda_origen.get()
        es_valido = self._modelo.intentar_asignar_peso(coord, texto_actual)

        if not es_valido:
            self._marcar_estado_celda(coord, tiene_error=True)
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
            text=f"✓ {total_aristas} aristas listas para generar",
            bg=COLOR_EXITO_FONDO,
            fg=COLOR_EXITO_TEXTO
        )

    def _evento_cargar_plantilla(self) -> None:
        self._modelo.cargar_plantilla_demostracion()
        self._sincronizar_vista_desde_modelo()

    def _evento_limpiar_matriz(self) -> None:
        self._modelo.limpiar_todo()
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
                "Corrija las celdas marcadas en rojo antes de guardar el grafo.",
                parent=self
            )
            return

        aristas = self._modelo.exportar_aristas()
        if not aristas:
            messagebox.showwarning(
                "Grafo sin aristas",
                "Ingrese al menos una conexión ponderada en la matriz.",
                parent=self
            )
            return

        for arista in aristas:
            self._config.grafo_destino.agregar_arista(arista.origen, arista.destino, arista.peso)

        self.destroy()
        self._config.al_confirmar()