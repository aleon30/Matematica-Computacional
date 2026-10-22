import tkinter as tk
from tkinter import ttk
from typing import Sequence
from estilos_tablas import aplicar_etiquetas_filas
from estrategias_tablas import ModeloFilaPaso


class TablaPasosModerna(ttk.Frame):
    """Componente modular profundo para visualizar el avance paso a paso."""

    def __init__(self, contenedor_padre: tk.Widget) -> None:
        super().__init__(contenedor_padre)
        self._construir_vista()
        self._configurar_columnas()
        aplicar_etiquetas_filas(self._arbol)


    def renderizar_pasos(self, filas: Sequence[ModeloFilaPaso]) -> None:
        """Inserta las filas y mantiene la vista fija en el paso actual."""
        self.limpiar()
        if not filas:
            return

        ultimo_id = None
        for indice, modelo in enumerate(filas):
            ultimo_id = self._insertar_fila(indice, modelo)

        if ultimo_id:
            self._arbol.see(ultimo_id)

    def limpiar(self) -> None:
        """Limpia todos los registros del árbol visual."""
        self._arbol.delete(*self._arbol.get_children())


    def _construir_vista(self) -> None:
        """Construye el Treeview y la barra de desplazamiento vertical."""
        self.pack(fill=tk.BOTH, expand=True)

        self._desplazamiento = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._arbol = ttk.Treeview(
            self,
            columns=("paso", "nodo", "vecino", "calculo", "decision"),
            show="headings",
            style="Moderno.Treeview",
            yscrollcommand=self._desplazamiento.set,
            selectmode="none",
            height=8
        )

        self._desplazamiento.config(command=self._arbol.yview)
        self._desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        self._arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _configurar_columnas(self) -> None:
        """Configura las 5 columnas centradas simétricamente como en el diseño original."""
        especificaciones = (
            ("paso", "Paso", 46, tk.CENTER),
            ("nodo", "Nodo", 44, tk.CENTER),
            ("vecino", "Vecino", 48, tk.CENTER),
            ("calculo", "Cálculo", 132, tk.CENTER),
            ("decision", "Decisión", 95, tk.CENTER)
        )

        for identificador, titulo, ancho, alineacion in especificaciones:
            self._arbol.heading(identificador, text=titulo, anchor=alineacion)
            self._arbol.column(identificador, width=ancho, anchor=alineacion)

    def _insertar_fila(self, indice: int, modelo: ModeloFilaPaso) -> str:
        """Inserta una fila aplicando fondo alternado y estilo de estado."""
        etiqueta_fondo = "fila_par" if indice % 2 == 0 else "fila_impar"
        etiquetas = (etiqueta_fondo, modelo.etiqueta_estilo)

        valores = (
            modelo.paso_id,
            modelo.nodo,
            modelo.vecino,
            modelo.calculo,
            modelo.decision_badge
        )
        return self._arbol.insert("", tk.END, values=valores, tags=etiquetas)