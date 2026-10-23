import tkinter as tk
from tkinter import ttk
from typing import Sequence, Protocol
from estilos_tablas import aplicar_etiquetas_filas


class IEstrategiaMatriz(Protocol):
    """Contrato Strategy para el formateo y alineación de celdas según el tipo de matriz."""
    def obtener_alineacion(self) -> str:
        ...
    def formatear_valor(self, fila: int, columna: int, valor: int) -> str:
        ...


class EstrategiaMatrizPesos(IEstrategiaMatriz):
    """Estrategia para la matriz de pesos ponderada."""
    def obtener_alineacion(self) -> str:
        # Números alineados a la derecha
        return tk.E

    def formatear_valor(self, fila: int, columna: int, valor: int) -> str:
        if valor >= 9999999:
            return "∞"
        return str(valor)


class EstrategiaMatrizBinaria(IEstrategiaMatriz):
    """Estrategia para matrices de adyacencia directa y caminos."""
    def obtener_alineacion(self) -> str:
        # Valores binarios centrados para lectura equilibrada
        return tk.CENTER

    def formatear_valor(self, fila: int, columna: int, valor: int) -> str:
        return str(valor)


class RegistroEstrategiasMatriz:
    """Registro que resuelve la estrategia en O(1) con complejidad ciclomática CC = 1."""
    def __init__(self) -> None:
        self._estrategias: dict[str, IEstrategiaMatriz] = {
            "pesos": EstrategiaMatrizPesos(),
            "directos": EstrategiaMatrizBinaria(),
            "accesibilidad": EstrategiaMatrizBinaria()
        }
        self._defecto = EstrategiaMatrizPesos()

    def resolver(self, tipo_vista: str) -> IEstrategiaMatriz:
        return self._estrategias.get(tipo_vista, self._defecto)


class TablaMatrizModerna(ttk.Frame):
    """
    Componente modular profundo para visualizar representaciones matriciales del grafo.
    Encapsula barras de desplazamiento bidireccionales, configuración dinámica de columnas
    y formateo de celdas.
    """

    def __init__(self, contenedor_padre: tk.Widget) -> None:
        super().__init__(contenedor_padre)
        self._registro = RegistroEstrategiasMatriz()
        self._construir_vista()
        aplicar_etiquetas_filas(self._arbol)
        self.mostrar_estado_vacio()


    def renderizar_matriz(self, matriz: Sequence[Sequence[int]], tipo_vista: str) -> None:
        """
        Reconfigura y llena la matriz bidimensional según la estrategia activa.
        Alinea valores numéricos y formatea infinitos y diagonales.
        """
        self.limpiar()
        if not matriz:
            self.mostrar_estado_vacio()
            return

        estrategia = self._registro.resolver(tipo_vista)
        total_vertices = len(matriz)

        self._reconfigurar_columnas(total_vertices, estrategia.obtener_alineacion())
        self._poblar_filas(matriz, estrategia)

    def mostrar_estado_vacio(self) -> None:
        """Presenta un estado neutral atenuado cuando aún no hay un grafo generado."""
        self.limpiar()
        self._arbol["columns"] = ("mensaje",)
        self._arbol.heading("mensaje", text="ESTADO DE MATRIZ", anchor=tk.CENTER)
        self._arbol.column("mensaje", width=380, anchor=tk.CENTER)
        self._arbol.insert(
            "",
            tk.END,
            values=("Genere o configure un grafo para visualizar su matriz",),
            tags=("estado_vacio",)
        )

    def limpiar(self) -> None:
        """Elimina todos los registros y columnas del árbol visual."""
        for item in self._arbol.get_children():
            self._arbol.delete(item)


    def _construir_vista(self) -> None:
        """Construye el Treeview con barras de desplazamiento vertical y horizontal."""
        self.pack(fill=tk.BOTH, expand=True)

        self._desplazamiento_y = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self._desplazamiento_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL)

        self._arbol = ttk.Treeview(
            self,
            show="headings",
            style="Moderno.Treeview",
            yscrollcommand=self._desplazamiento_y.set,
            xscrollcommand=self._desplazamiento_x.set,
            selectmode="none"
        )

        self._desplazamiento_y.config(command=self._arbol.yview)
        self._desplazamiento_x.config(command=self._arbol.xview)

        self._desplazamiento_y.pack(side=tk.RIGHT, fill=tk.Y)
        self._desplazamiento_x.pack(side=tk.BOTTOM, fill=tk.X)
        self._arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _reconfigurar_columnas(self, total_vertices: int, alineacion_datos: str) -> None:
        """Configura la columna de origen y las columnas dinámicas de destino."""
        nombres_columnas = ["origen"] + [f"dest_{i}" for i in range(total_vertices)]
        self._arbol["columns"] = nombres_columnas

        # Columna de Origen
        self._arbol.heading("origen", text="ORIGEN \\ DESTINO", anchor=tk.CENTER)
        self._arbol.column("origen", width=120, anchor=tk.CENTER, stretch=False)

        # Columnas de Destino numeradas
        ancho_columna = 55 if total_vertices > 8 else 70
        for i in range(total_vertices):
            col_id = f"dest_{i}"
            self._arbol.heading(col_id, text=f"[{i}]", anchor=alineacion_datos)
            self._arbol.column(col_id, width=ancho_columna, anchor=alineacion_datos, stretch=True)

    def _poblar_filas(self, matriz: Sequence[Sequence[int]], estrategia: IEstrategiaMatriz) -> None:
        """Inserta las filas de la matriz aplicando el patrón zebra de diseño."""
        for fila_idx, fila_datos in enumerate(matriz):
            etiqueta_fondo = "fila_par" if fila_idx % 2 == 0 else "fila_impar"
            valores_fila = [f"Nodo [{fila_idx}]"]

            for col_idx, valor_celda in enumerate(fila_datos):
                valor_formateado = estrategia.formatear_valor(fila_idx, col_idx, valor_celda)
                valores_fila.append(valor_formateado)

            self._arbol.insert("", tk.END, values=valores_fila, tags=(etiqueta_fondo,))