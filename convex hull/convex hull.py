import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Tuple
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definición de tipo para puntos
Point = Tuple[float, float]

# --- LÓGICA DEL CONVEX HULL (Igual que antes) ---

def leer_puntos_csv(ruta_csv: str) -> List[Point]:
    """Lee un CSV con encabezados x,y."""
    puntos: List[Point] = []
    try:
        with open(ruta_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                x = float(row["x"])
                y = float(row["y"])
                puntos.append((x, y))
    except Exception as e:
        print(f"Error leyendo CSV: {e}")
        return []
    return puntos

def punto_mas_izquierdo(puntos: List[Point]) -> int:
    idx = 0
    for i in range(1, len(puntos)):
        if puntos[i][0] < puntos[idx][0] or (puntos[i][0] == puntos[idx][0] and puntos[i][1] < puntos[idx][1]):
            idx = i
    return idx

def orientacion(a: Point, b: Point, c: Point) -> float:
    # Retorna: > 0 Antihorario, < 0 Horario, 0 Colineal
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

def distancia2(a: Point, b: Point) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

def convex_hull(puntos: List[Point]) -> List[Point]:
    n = len(puntos)
    if n < 3: return puntos[:]
    
    hull = []
    start_idx = punto_mas_izquierdo(puntos)
    p_idx = start_idx
    
    while True:
        hull.append(puntos[p_idx])
        q_idx = (p_idx + 1) % n
        
        for r_idx in range(n):
            if r_idx == p_idx: continue
            
            val = orientacion(puntos[p_idx], puntos[q_idx], puntos[r_idx])
            
            if val > 0: # r está a la izquierda de pq
                q_idx = r_idx
            elif val == 0: # Colineales, tomar el más lejano
                if distancia2(puntos[p_idx], puntos[r_idx]) > distancia2(puntos[p_idx], puntos[q_idx]):
                    q_idx = r_idx
        
        p_idx = q_idx
        if p_idx == start_idx:
            break
            
    return hull

# --- INTERFAZ GRÁFICA (GUI) ---

def cargar_y_graficar():
    # 1. Abrir diálogo para seleccionar archivo
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo CSV",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return # Usuario canceló

    # 2. Procesar lógica
    try:
        puntos = leer_puntos_csv(ruta_archivo)
        if not puntos:
            messagebox.showerror("Error", "El archivo está vacío o mal formado.")
            return

        hull = convex_hull(puntos)
        
        # 3. Actualizar etiqueta de info
        lbl_info.config(text=f"Puntos cargados: {len(puntos)} | Vértices en Hull: {len(hull)}")

        # 4. Dibujar en el Canvas de Tkinter
        ax.clear() # Limpiar gráfica anterior
        
        # Datos
        xs = [p[0] for p in puntos]
        ys = [p[1] for p in puntos]
        
        # Graficar puntos
        ax.scatter(xs, ys, color='blue', label='Puntos')
        
        # Graficar Hull
        if len(hull) >= 2:
            hx = [p[0] for p in hull] + [hull[0][0]]
            hy = [p[1] for p in hull] + [hull[0][1]]
            ax.plot(hx, hy, 'r-', linewidth=2, label='Convex Hull')
            ax.scatter(hx, hy, color='red', s=50, zorder=5)

        ax.set_title("Visualización Convex Hull")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Refrescar el canvas
        canvas.draw()
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora Convex Hull")
root.geometry("800x600")

# Marco superior para controles
frame_top = tk.Frame(root, pady=10)
frame_top.pack(side=tk.TOP, fill=tk.X)

btn_cargar = tk.Button(frame_top, text="Cargar CSV y Calcular", command=cargar_y_graficar, bg="#4CAF50", fg="white", font=("Arial", 12))
btn_cargar.pack(pady=5)

lbl_info = tk.Label(frame_top, text="Selecciona un archivo para comenzar", font=("Arial", 10))
lbl_info.pack()

# Marco para la gráfica
frame_grafica = tk.Frame(root)
frame_grafica.pack(fill=tk.BOTH, expand=True)

# Inicializar figura de Matplotlib
fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Iniciar loop de la GUI
root.mainloop()