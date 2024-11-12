import tkinter as tk
from tkinter import messagebox, ttk
from igraph import Graph, plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración inicial de la matriz de adyacencia y otros parámetros
adj_matrix = [
    [0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 0]
]

# Paleta ampliada de colores
palette = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta", "brown", "gray"]

def min_colors_vizing(graph):
    """
    Calcula el número mínimo de colores necesarios según el teorema de Vizing.
    Args:
        graph (Graph): El grafo a analizar.
    Returns:
        int: Número mínimo de colores necesarios.
    """
    max_degree = max(graph.degree())
    return max_degree + 1

def is_safe_edge(edge, color, colors, graph):
    u = edge.source
    v = edge.target
    for neighbor_edge in graph.es:
        if (neighbor_edge.source == u or neighbor_edge.target == u or 
            neighbor_edge.source == v or neighbor_edge.target == v):
            # Verificar que no haya arista adyacente con el mismo color
            if colors[neighbor_edge.index] == color:
                return False
    return True

def edge_coloring(graph, num_colors, colors, edge_order):
    """
    Algoritmo mejorado de backtracking para colorear las aristas del grafo,
    asignando colores a cada arista sin que dos aristas adyacentes tengan el mismo color.
    """
    for edge_index in edge_order:
        for color in range(num_colors):
            if is_safe_edge(graph.es[edge_index], color, colors, graph):
                colors[edge_index] = color
                break
        else:
            return False  # Si no se puede asignar un color, retorna False
    return True

def update_graph(directed=True):
    """
    Actualiza la visualización del grafo en la GUI, coloreando las aristas
    en función de la matriz de adyacencia y el número de colores necesarios.
    """
    global adj_matrix
    g = Graph.Adjacency(adj_matrix)
    if not directed:
        g.to_undirected()  # Convierte el grafo a no dirigido

    # Calcula el número mínimo de colores según el teorema de Vizing
    required_colors = min_colors_vizing(g)
    num_colors = max(required_colors, len(palette))  # Asegura suficientes colores en la paleta

    # Ordenar aristas por el grado de sus nodos extremos (heurística)
    edge_degrees = [(edge.index, g.degree(edge.source) + g.degree(edge.target)) for edge in g.es]
    edge_order = [index for index, degree in sorted(edge_degrees, key=lambda x: -x[1])]
    
    colors = [-1] * len(g.es)  # Inicializamos todas las aristas con color -1
    
    if edge_coloring(g, num_colors, colors, edge_order):
        g.es["color"] = [palette[color % len(palette)] for color in colors]
        fig, ax = plt.subplots(figsize=(7, 7))
        plot(g, target=ax, vertex_size=40, vertex_color='lightblue', vertex_label=range(len(g.vs)),
             edge_width=2, edge_color=g.es["color"])
        ax.set_title("Coloración de las Aristas del Grafo (" + ("Dirigido" if directed else "No Dirigido") + ")")
        
        # Mostrar el gráfico en la GUI
        for widget in frame_graph.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", f"No es posible colorear las aristas del grafo con {num_colors} colores.")

def update_matrix():
    global adj_matrix
    try:
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix)):
                value = int(entry_matrix[i][j].get())
                if value not in (0, 1):
                    raise ValueError("Los valores deben ser 0 o 1.")
                adj_matrix[i][j] = value
        update_graph()
    except ValueError as e:
        messagebox.showerror("Entrada inválida", str(e))

# Crear la ventana principal
window = tk.Tk()
window.title("Coloración de Aristas de Grafo - GUI Mejorada")
window.geometry("1000x800")

# Crear el marco para la matriz de adyacencia
frame_matrix = tk.LabelFrame(window, text="Matriz de Adyacencia", padx=10, pady=10)
frame_matrix.grid(row=0, column=0, padx=20, pady=20)

# Crear los campos de entrada para la matriz de adyacencia
entry_matrix = []
for i in range(len(adj_matrix)):
    row_entries = []
    for j in range(len(adj_matrix[i])):
        entry = tk.Entry(frame_matrix, width=7, justify="center", font=("Arial", 14))
        entry.insert(0, str(adj_matrix[i][j]))
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
    entry_matrix.append(row_entries)

# Botón para actualizar la matriz de adyacencia y colorear el grafo
update_button = tk.Button(window, text="Actualizar Matriz y Colorear Aristas", command=update_matrix, font=("Arial", 14))
update_button.grid(row=1, column=0, pady=20)

# Crear el marco para la visualización del grafo
frame_graph = tk.LabelFrame(window, text="Visualización del Grafo", padx=10, pady=10)
frame_graph.grid(row=0, column=1, rowspan=2, padx=20, pady=20)

# Agregar botones para elegir si el grafo es dirigido o no dirigido
directed_button = tk.Button(window, text="Mostrar Grafo Dirigido", command=lambda: update_graph(directed=True), font=("Arial", 12))
directed_button.grid(row=2, column=0, pady=10)

undirected_button = tk.Button(window, text="Mostrar Grafo No Dirigido", command=lambda: update_graph(directed=False), font=("Arial", 12))
undirected_button.grid(row=3, column=0, pady=10)

# Mostrar la coloración inicial del grafo
update_graph()

# Iniciar el bucle principal de la GUI
window.mainloop()
