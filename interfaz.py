import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from Grafo import Grafo
from dibujarGrafo_gui import dibujar_en_canvas

class AplicacionGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Camino Minimo")
        self.root.geometry("950x700")
        self.root.configure(bg="#FFFFFF")
        
        self.grafo_actual = None
        
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
        
        self.panel_principal = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=COLOR_FONDO, borderwidth=0)
        self.panel_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.frame_controles = ttk.Frame(self.panel_principal, padding="20 10 30 10")
        self.panel_principal.add(self.frame_controles, minsize=380, stretch="never")
        
        self.frame_grafico = ttk.Frame(self.panel_principal, padding="10")
        self.panel_principal.add(self.frame_grafico, minsize=500, stretch="always")
        
        self.crear_controles()
        self.crear_estado_vacio()
        
    def crear_estado_vacio(self):
        # Mensaje sutil para rellenar el espacio vacio inicial
        self.label_vacio = ttk.Label(self.frame_grafico, text="El grafo visualizado aparecera aqui", font=("Helvetica", 12), foreground="#7A7A7A")
        self.label_vacio.place(relx=0.5, rely=0.5, anchor="center")
        
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
        
        self.texto_pasos = tk.Text(self.frame_texto, height=8, width=30, yscrollcommand=self.scroll_texto.set, state="disabled", 
                                   font=("Consolas", 9), bg="#F8FAFC", fg="#475569", relief="flat", highlightthickness=1, highlightbackground="#E2E8F0")
        self.texto_pasos.pack(side="left", fill="both", expand=True)
        self.scroll_texto.config(command=self.texto_pasos.yview)
        
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
        
        if metodo == "auto":
            for i in range(num_vertices):
                for j in range(i + 1, num_vertices):
                    if random.random() > 0.3: 
                        peso = random.randint(1, 50)
                        self.grafo_actual.agregar_arista(i, j, peso)
                        
            self.label_resultado.config(text="Estado: Grafo generado automaticamente.", style='Exito.TLabel')
            self.limpiar_paso_a_paso()
            dibujar_en_canvas(self.grafo_actual.aristas, [], self.frame_grafico)
            
        elif metodo == "manual":
            self.abrir_ventana_manual(num_vertices)

    def abrir_ventana_manual(self, num_vertices):
        ventana_manual = tk.Toplevel(self.root)
        ventana_manual.title("Ingreso Manual")
        ventana_manual.geometry("350x500")
        ventana_manual.configure(bg="#FFFFFF")
        
        canvas_scroll = tk.Canvas(ventana_manual, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana_manual, orient="vertical", command=canvas_scroll.yview)
        frame_interior = ttk.Frame(canvas_scroll)
        
        frame_interior.bind("<Configure>", lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all")))
        canvas_scroll.create_window((0, 0), window=frame_interior, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)
        
        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Label(frame_interior, text="Magnitud de las conexiones", style='Titulo.TLabel').pack(pady=(20, 5))
        ttk.Label(frame_interior, text="Indique 0 si no hay conexion directa.", style='Secundario.TLabel').pack(pady=(0, 20))
        
        entradas_pesos = {}
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                frame_fila = ttk.Frame(frame_interior)
                frame_fila.pack(fill="x", padx=30, pady=4)
                ttk.Label(frame_fila, text=f"Nodo {i} a Nodo {j}:").pack(side="left")
                entry = ttk.Entry(frame_fila, width=8, font=("Helvetica", 10))
                entry.insert(0, "0")
                entry.pack(side="right")
                entradas_pesos[(i, j)] = entry
                
        def guardar_pesos():
            for (i, j), entry in entradas_pesos.items():
                try:
                    peso = int(entry.get())
                    if peso > 0:
                        self.grafo_actual.agregar_arista(i, j, peso)
                    elif peso < 0:
                        messagebox.showwarning("Aviso", f"El valor negativo entre {i} y {j} fue omitido.")
                except ValueError:
                    pass
            ventana_manual.destroy()
            self.label_resultado.config(text="Estado: Grafo manual generado exitosamente.", style='Exito.TLabel')
            self.limpiar_paso_a_paso()
            dibujar_en_canvas(self.grafo_actual.aristas, [], self.frame_grafico)
            
        ttk.Button(frame_interior, text="Guardar y Visualizar", style='Primario.TButton', command=guardar_pesos).pack(pady=30)

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
        
        if self.grafo_actual.recorrido_minimo == [-1]:
            texto_res = "Resultado: No existe un camino posible."
            self.label_resultado.config(text=texto_res, foreground="#0A0A0A")
        else:
            texto_res = f"Ruta: {self.grafo_actual.recorrido_minimo}\nCosto Total: {self.grafo_actual.costo_total}"
            self.label_resultado.config(text=texto_res, style='Exito.TLabel')
            
        self.mostrar_paso_a_paso(self.grafo_actual.historial_pasos)
        dibujar_en_canvas(self.grafo_actual.aristas, self.grafo_actual.recorrido_minimo, self.frame_grafico)

    def mostrar_paso_a_paso(self, texto):
        self.texto_pasos.config(state="normal")
        self.texto_pasos.delete(1.0, tk.END)
        self.texto_pasos.insert(tk.END, texto)
        self.texto_pasos.config(state="disabled")

    def limpiar_paso_a_paso(self):
        self.texto_pasos.config(state="normal")
        self.texto_pasos.delete(1.0, tk.END)
        self.texto_pasos.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionGrafo(root)
    root.mainloop()