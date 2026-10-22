import tkinter as tk
from tkinter import ttk
from typing import Sequence, Tuple
from estilos_tablas import aplicar_etiquetas_filas, COLOR_GRIS_700, COLOR_FONDO_BASE


class TablaColaModerna(ttk.Frame):
    """
    Componente modular profundo para visualizar la cola de prioridad.
    Usa un contenedor plano con título superior limpio, eliminando el borde mostaza de LabelFrame.
    """

    def __init__(self, contenedor_padre: tk.Widget) -> None:
        super().__init__(contenedor_padre, style='TFrame')
        self._construir_titulo()
        self._construir_vista()
        self._configurar_columnas()
        aplicar_etiquetas_filas(self._arbol)
        self.mostrar_estado_vacio()

    # Interfaz Pública Mínima (Modularidad Profunda - John Ousterhout)

    def actualizar_elementos(self, elementos: Sequence[Tuple[int, int, int]]) -> None:
        """
        Actualiza el contenido de la cola de prioridad.
        Si la lista está vacía, muestra automáticamente el estado vacío atenuado.
        """
        self.limpiar()
        if not elementos:
            self.mostrar_estado_vacio()
            return

        for indice, elemento in enumerate(elementos):
            self._insertar_elemento(indice, elemento)

    def mostrar_estado_vacio(self) -> None:
        """Muestra una fila semántica que indica que la cola no contiene elementos."""
        self.limpiar()
        self._arbol.insert(
            "",
            tk.END,
            values=("—", "Cola vacía", "—"),
            tags=("estado_vacio",)
        )

    def limpiar(self) -> None:
        """Limpia los elementos del árbol visual."""
        self._arbol.delete(*self._arbol.get_children())

    # Métodos Privados y Ocultamiento de Información

    def _construir_titulo(self) -> None:
        """Construye un título limpio y des-enfatizado sin el marco biselado antiguo."""
        self._etiqueta_titulo = ttk.Label(
            self,
            text="Cola de prioridad (costo, nodo, predecesor)",
            font=("Helvetica", 9, "bold"),
            foreground=COLOR_GRIS_700,
            background=COLOR_FONDO_BASE
        )
        self._etiqueta_titulo.pack(anchor=tk.W, pady=(0, 6))

    def _construir_vista(self) -> None:
        """Construye y empaqueta el Treeview y su barra de desplazamiento."""
        self.pack(fill=tk.X, pady=(0, 10))

        self._desplazamiento = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._arbol = ttk.Treeview(
            self,
            columns=("costo", "nodo", "predecesor"),
            show="headings",
            style="Moderno.Treeview",
            yscrollcommand=self._desplazamiento.set,
            selectmode="none",
            height=3
        )

        self._desplazamiento.config(command=self._arbol.yview)
        self._desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        self._arbol.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _configurar_columnas(self) -> None:
        """
        Configura cabeceras y anchos fijos.
        Alinea el costo numérico a la derecha (anchor='e') y los nodos al centro.
        """
        especificaciones = (
            ("costo", "COSTO", 80, tk.E),
            ("nodo", "NODO", 70, tk.CENTER),
            ("predecesor", "ORIGEN / PREVIO", 110, tk.CENTER)
        )

        for identificador, titulo, ancho, alineacion in especificaciones:
            self._arbol.heading(identificador, text=titulo, anchor=alineacion)
            self._arbol.column(identificador, width=ancho, anchor=alineacion)

    def _insertar_elemento(self, indice: int, elemento: Tuple[int, int, int]) -> None:
        """Inserta una fila individual aplicando fondo alternado y estilo semántico."""
        costo, predecesor, nodo = elemento
        etiqueta_fondo = "fila_par" if indice % 2 == 0 else "fila_impar"
        etiquetas = (etiqueta_fondo, "estado_encolada")

        origen_texto = f"Nodo [{predecesor}]" if predecesor != -1 else "Inicio"
        valores = (
            f"{costo}",
            f"[{nodo}]",
            origen_texto
        )
        self._arbol.insert("", tk.END, values=valores, tags=etiquetas)