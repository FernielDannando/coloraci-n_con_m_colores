import tkinter as tk
from tkinter import messagebox
from igraph import Graph, plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración inicial de la matriz de adyacencia y paleta de colores
adj_matrix = [
    [0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 1, 1],
    [0, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 1, 0]
]
palette = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta", "brown", "gray"]

def min_colors_vizing(graph):
    max_degree = max(graph.degree())
    return max_degree + 1

def edge_coloring(graph, num_colors, colors, edge_order):
    for edge_index in edge_order:
        for color in range(num_colors):
            if is_safe_edge(graph.es[edge_index], color, colors, graph):
                colors[edge_index] = color
                break
        else:
            return False
    return True

def is_safe_edge(edge, color, colors, graph):
    u, v = edge.source, edge.target
    for neighbor_edge in graph.es:
        if (neighbor_edge.source in (u, v) or neighbor_edge.target in (u, v)) and colors[neighbor_edge.index] == color:
            return False
    return True

def color_edges():
    g = Graph.Adjacency(adj_matrix)
    g.to_undirected()
    required_colors = min_colors_vizing(g)
    num_colors = max(required_colors, len(palette))
    edge_degrees = [(edge.index, g.degree(edge.source) + g.degree(edge.target)) for edge in g.es]
    edge_order = [index for index, degree in sorted(edge_degrees, key=lambda x: -x[1])]
    colors = [-1] * len(g.es)
    
    if edge_coloring(g, num_colors, colors, edge_order):
        g.es["color"] = [palette[color % len(palette)] for color in colors]
        display_graph(g, "Coloración de Aristas")

def is_safe_vertex(node, color, colors, graph):
    for neighbor in graph.neighbors(node):
        if colors[neighbor] == color:
            return False
    return True

def vertex_coloring(graph, num_colors, colors, node=0):
    if node == len(graph.vs):
        return True
    for color in range(num_colors):
        if is_safe_vertex(node, color, colors, graph):
            colors[node] = color
            if vertex_coloring(graph, num_colors, colors, node + 1):
                return True
            colors[node] = -1
    return False

def color_vertices():
    g = Graph.Adjacency(adj_matrix)
    g.to_undirected()
    colors = [-1] * len(g.vs)
    if vertex_coloring(g, len(palette), colors):
        g.vs["color"] = [palette[color % len(palette)] for color in colors]
        display_graph(g, "Coloración de Vértices")

def display_graph(graph, title):
    fig, ax = plt.subplots(figsize=(7, 7))
    plot(graph, target=ax, vertex_size=40, vertex_color=graph.vs["color"] if "color" in graph.vs.attributes() else "lightblue",
         vertex_label=range(len(graph.vs)), edge_width=2, edge_color=graph.es["color"] if "color" in graph.es.attributes() else "black")
    ax.set_title(title)
    
    for widget in frame_graph.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack()

def update_matrix():
    global adj_matrix
    try:
        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix)):
                value = int(entry_matrix[i][j].get())
                if value not in (0, 1):
                    raise ValueError("Los valores deben ser 0 o 1.")
                adj_matrix[i][j] = value
    except ValueError as e:
        messagebox.showerror("Entrada inválida", str(e))

# Configuración de la GUI
window = tk.Tk()
window.title("Coloración de Aristas y Vértices de Grafo")
window.geometry("1000x800")

# Frame para la matriz de adyacencia
frame_matrix = tk.LabelFrame(window, text="Matriz de Adyacencia", padx=10, pady=10)
frame_matrix.grid(row=0, column=0, padx=20, pady=20)

# Entradas para la matriz de adyacencia
entry_matrix = []
for i in range(len(adj_matrix)):
    row_entries = []
    for j in range(len(adj_matrix[i])):
        entry = tk.Entry(frame_matrix, width=5, justify="center")
        entry.insert(0, str(adj_matrix[i][j]))
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
    entry_matrix.append(row_entries)

# Botones para colorear el grafo
update_button = tk.Button(window, text="Actualizar Matriz", command=update_matrix)
update_button.grid(row=1, column=0, pady=20)

edge_button = tk.Button(window, text="Colorear Aristas", command=color_edges)
edge_button.grid(row=2, column=0, pady=10)

vertex_button = tk.Button(window, text="Colorear Vértices", command=color_vertices)
vertex_button.grid(row=3, column=0, pady=10)

# Frame para mostrar el grafo
frame_graph = tk.LabelFrame(window, text="Visualización del Grafo", padx=10, pady=10)
frame_graph.grid(row=0, column=1, rowspan=4, padx=20, pady=20)

# Iniciar la GUI
window.mainloop()
