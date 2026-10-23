from tkinter import ttk
import tkinter as tk

COLOR_FONDO_BASE = "#FFFFFF"       # Blanco puro de celda
COLOR_GRIS_100   = "#F8FAFC"       # Fondo alternado de fila y pista de scrollbar
COLOR_GRIS_200   = "#E2E8F0"       # Separadores sutiles y bordes planos
COLOR_GRIS_300   = "#CBD5E1"       # Barra móvil de scrollbar (pulgar)
COLOR_GRIS_400   = "#94A3B8"       # Textos atenuados / scrollbar en hover
COLOR_GRIS_500   = "#64748B"       # Texto secundario de cabeceras y flechas
COLOR_GRIS_700   = "#334155"       # Iconos y títulos de sección
COLOR_GRIS_800   = "#1E293B"       # Texto primario de lectura en celdas

# Primario (Azul Marca - Hue 220°)
COLOR_PRIMARIO_100 = "#DBEAFE"     # Fondo suave para badge encolado
COLOR_PRIMARIO_900 = "#1E3A8A"     # Texto de alto contraste para encolado

# Semánticos: Éxito (145°), Advertencia (42°), Peligro (355°)
COLOR_EXITO_FONDO   = "#DCFCE7"    # Fondo de estado alcanzado/éxito
COLOR_EXITO_TEXTO   = "#14532D"    # Texto de estado alcanzado/éxito

COLOR_AVISO_FONDO   = "#FEF3C7"    # Fondo de advertencia/atención
COLOR_AVISO_TEXTO   = "#78350F"    # Texto de advertencia/atención

COLOR_PELIGRO_FONDO = "#FEE2E2"    # Fondo de descarte/error
COLOR_PELIGRO_TEXTO = "#7F1D1D"    # Texto de descarte/error

# -------------------------------------------------------------------------
# Tipografía y Espaciado (Escala cerrada)
# -------------------------------------------------------------------------
ALTURA_FILA_TABLA = 36             # Altura para soportar 2 líneas limpiamente
FUENTE_CABECERA   = ("Helvetica", 9, "bold")
FUENTE_CELDA      = ("Helvetica", 9)


def configurar_estilos_tablas(estilo: ttk.Style) -> None:
    """
    Configura el tema unificado para tablas, cabeceras, barras de desplazamiento
    y marcos contenedores, eliminando los colores mostaza y biseles 3D antiguos.
    """
    # 1. Cuerpo de la tabla (Treeview)
    estilo.configure(
        "Moderno.Treeview",
        background=COLOR_FONDO_BASE,
        foreground=COLOR_GRIS_800,
        fieldbackground=COLOR_FONDO_BASE,
        rowheight=ALTURA_FILA_TABLA,
        font=FUENTE_CELDA,
        borderwidth=0,
        relief="flat"
    )
    estilo.map(
        "Moderno.Treeview",
        background=[("selected", COLOR_GRIS_200)],
        foreground=[("selected", COLOR_GRIS_800)]
    )

    # 2. Encabezados de la tabla (Treeview Heading)
    estilo.configure(
        "Moderno.Treeview.Heading",
        background=COLOR_GRIS_100,
        foreground=COLOR_GRIS_500,
        font=FUENTE_CABECERA,
        borderwidth=0,
        relief="flat"
    )
    estilo.map(
        "Moderno.Treeview.Heading",
        background=[("active", COLOR_GRIS_200)],
        foreground=[("active", COLOR_GRIS_700)]
    )

    # 3. Barras de desplazamiento modernas
    estilo.configure(
        "TScrollbar",
        background=COLOR_GRIS_300,
        troughcolor=COLOR_GRIS_100,
        bordercolor=COLOR_FONDO_BASE,
        arrowcolor=COLOR_GRIS_500,
        lightcolor=COLOR_GRIS_300,
        darkcolor=COLOR_GRIS_300,
        arrowsize=11,
        relief="flat"
    )
    estilo.map(
        "TScrollbar",
        background=[("pressed", COLOR_GRIS_700), ("active", COLOR_GRIS_400)],
        arrowcolor=[("pressed", COLOR_GRIS_800), ("active", COLOR_GRIS_700)]
    )

    estilo.configure(
        "Vertical.TScrollbar",
        background=COLOR_GRIS_300,
        troughcolor=COLOR_GRIS_100,
        bordercolor=COLOR_FONDO_BASE,
        arrowcolor=COLOR_GRIS_500,
        lightcolor=COLOR_GRIS_300,
        darkcolor=COLOR_GRIS_300,
        arrowsize=11,
        relief="flat"
    )
    estilo.map(
        "Vertical.TScrollbar",
        background=[("pressed", COLOR_GRIS_700), ("active", COLOR_GRIS_400)],
        arrowcolor=[("pressed", COLOR_GRIS_800), ("active", COLOR_GRIS_700)]
    )

    estilo.configure(
        "Horizontal.TScrollbar",
        background=COLOR_GRIS_300,
        troughcolor=COLOR_GRIS_100,
        bordercolor=COLOR_FONDO_BASE,
        arrowcolor=COLOR_GRIS_500,
        lightcolor=COLOR_GRIS_300,
        darkcolor=COLOR_GRIS_300,
        arrowsize=11,
        relief="flat"
    )
    estilo.map(
        "Horizontal.TScrollbar",
        background=[("pressed", COLOR_GRIS_700), ("active", COLOR_GRIS_400)],
        arrowcolor=[("pressed", COLOR_GRIS_800), ("active", COLOR_GRIS_700)]
    )

    # 4. Marcos contenedores
    estilo.configure(
        "TLabelframe",
        background=COLOR_FONDO_BASE,
        bordercolor=COLOR_GRIS_200,
        lightcolor=COLOR_FONDO_BASE,
        darkcolor=COLOR_FONDO_BASE,
        relief="flat",
        borderwidth=0
    )
    estilo.configure(
        "TLabelframe.Label",
        background=COLOR_FONDO_BASE,
        foreground=COLOR_GRIS_700,
        font=FUENTE_CABECERA
    )

    #5
    estilo.configure(
        "TCombobox",
        background=COLOR_FONDO_BASE,       # Fondo del botón de la flecha blanco unificado
        foreground=COLOR_GRIS_800,        # Color del texto seleccionado
        fieldbackground=COLOR_FONDO_BASE, # Fondo de la caja de texto
        bordercolor=COLOR_GRIS_300,       # Borde sutil plano (1px)
        darkcolor=COLOR_FONDO_BASE,       # Elimina biseles oscuros 3D
        lightcolor=COLOR_FONDO_BASE,      # Elimina brillos 3D
        arrowcolor=COLOR_GRIS_500,        # Flecha moderna en gris pizarra suave
        arrowsize=11,                     # Tamaño proporcional de la flecha
        relief="flat",
        padding=[10, 6]                   # Espaciado interno cómodo (space-2 / space-3)
    )

    estilo.map(
        "TCombobox",
        fieldbackground=[
            ("readonly", COLOR_FONDO_BASE),
            ("disabled", COLOR_GRIS_100)
        ],
        background=[
            ("active", COLOR_GRIS_100),    # Micro-hover sutil en el botón
            ("pressed", COLOR_GRIS_200),
            ("readonly", COLOR_FONDO_BASE)
        ],
        arrowcolor=[
            ("active", COLOR_PRIMARIO_900), # La flecha se ilumina en azul marca
            ("pressed", COLOR_PRIMARIO_900),
            ("disabled", COLOR_GRIS_400)
        ],
        bordercolor=[
            ("focus", COLOR_PRIMARIO_900),  # Anillo de foco azul al seleccionar
            ("active", COLOR_GRIS_400)
        ],
        lightcolor=[
            ("focus", COLOR_PRIMARIO_900),
            ("active", COLOR_FONDO_BASE)
        ],
        darkcolor=[
            ("focus", COLOR_PRIMARIO_900),
            ("active", COLOR_FONDO_BASE)
        ]
    )


def aplicar_etiquetas_filas(arbol: ttk.Treeview) -> None:
    """Aplica las etiquetas de alternancia de filas y estados semánticos."""
    arbol.tag_configure("fila_par", background=COLOR_FONDO_BASE)
    arbol.tag_configure("fila_impar", background=COLOR_GRIS_100)

    arbol.tag_configure("estado_visita", foreground=COLOR_PRIMARIO_900)
    arbol.tag_configure("estado_encolada", foreground=COLOR_GRIS_700)
    arbol.tag_configure("estado_descarte", foreground=COLOR_PELIGRO_TEXTO)
    arbol.tag_configure("estado_destino", foreground=COLOR_EXITO_TEXTO)
    arbol.tag_configure("estado_vacio", foreground=COLOR_GRIS_400)

def configurar_estilos_desplegable_popdown(root: tk.Tk) -> None:
    """
    Estiliza la lista flotante de opciones (el menú desplegable que se abre)
    para que coincida con la tipografía y colores suaves del sistema de diseño.
    """
    root.option_add('*TCombobox*Listbox.font', FUENTE_CELDA)
    root.option_add('*TCombobox*Listbox.background', COLOR_FONDO_BASE)
    root.option_add('*TCombobox*Listbox.foreground', COLOR_GRIS_800)
    root.option_add('*TCombobox*Listbox.selectBackground', COLOR_PRIMARIO_100) # Fondo azul suave
    root.option_add('*TCombobox*Listbox.selectForeground', COLOR_PRIMARIO_900) # Texto azul oscuro
    root.option_add('*TCombobox*Listbox.relief', 'flat')
    root.option_add('*TCombobox*Listbox.borderWidth', 1)