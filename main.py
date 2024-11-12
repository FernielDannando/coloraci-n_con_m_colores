"""
Este módulo proporciona una interfaz gráfica de usuario (GUI) para la coloración de grafos
utilizando un algoritmo de backtracking. Permite al usuario ingresar una matriz de adyacencia
y visualizar la coloración del grafo resultante en una gráfica, tanto en forma dirigida como no dirigida.
"""

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

num_colors = 4
palette = ["red", "green", "blue", "yellow"]

def is_safe(node, color, colors, graph):
    """
    Verifica si es seguro asignar un color al nodo dado, asegurándose de que
    ningún nodo adyacente tenga el mismo color.

    Args:
        node (int): El nodo actual a colorear.
        color (int): El color a asignar al nodo.
        colors (list): Lista de colores asignados a cada nodo.
        graph (Graph): El grafo que representa la matriz de adyacencia.

    Returns:
        bool: True si es seguro colorear el nodo con el color dado, de lo contrario False.
    """
    for neighbor in graph.neighbors(node):
        if colors[neighbor] == color:
            return False
    return True

def graph_coloring(graph, num_colors, colors, node=0):
    """
    Algoritmo de backtracking para colorear un grafo, asignando colores a cada nodo
    sin que dos nodos adyacentes tengan el mismo color.

    Args:
        graph (Graph): El grafo a colorear.
        num_colors (int): Número de colores disponibles.
        colors (list): Lista de colores asignados a cada nodo.
        node (int): Nodo actual en proceso de coloración.

    Returns:
        bool: True si el grafo se coloreó con éxito, de lo contrario False.
    """
    if node == len(graph.vs):
        return True
    for color in range(num_colors):
        if is_safe(node, color, colors, graph):
            colors[node] = color
            if graph_coloring(graph, num_colors, colors, node + 1):
                return True
            colors[node] = -1  # Backtrack
    return False

def update_graph(directed=True):
    """
    Actualiza la visualización del grafo en la GUI, coloreando los nodos
    en función de la matriz de adyacencia y el número de colores disponibles.
    También se puede visualizar como un grafo no dirigido.
    
    Args:
        directed (bool): Si es True, visualiza el grafo dirigido, si es False, lo visualiza no dirigido.
    """
    global adj_matrix
    g = Graph.Adjacency(adj_matrix)
    if not directed:
        g.to_undirected()  # Convierte el grafo a no dirigido
    colors = [-1] * len(g.vs)
    
    if graph_coloring(g, num_colors, colors):
        # Verifica que no se asignen más colores que los disponibles en la paleta
        g.vs["color"] = [palette[color % num_colors] for color in colors]  # Usa el operador % para evitar desbordamiento de colores
        fig, ax = plt.subplots(figsize=(7, 7))  # Tamaño de la figura aumentado
        plot(g, target=ax, vertex_size=40, vertex_color=g.vs["color"], vertex_label=range(len(g.vs)),
             edge_width=0.8, edge_color='gray')
        ax.set_title("Coloración del Grafo (" + ("Dirigido" if directed else "No Dirigido") + ")")
        
        # Mostrar el gráfico en la GUI
        for widget in frame_graph.winfo_children():
            widget.destroy()  # Limpiar gráficos anteriores
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", f"No es posible colorear el grafo con {num_colors} colores.")

def update_matrix():
    """
    Actualiza la matriz de adyacencia en función de los valores ingresados en la GUI,
    y luego actualiza la visualización del grafo en función de la nueva matriz.
    """
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
window.title("Coloración de nodos de un Grafo")
window.geometry("1000x800")  # Dimensiones aumentadas

# Crear el marco para la matriz de adyacencia
frame_matrix = tk.LabelFrame(window, text="Matriz de Adyacencia", padx=10, pady=10)
frame_matrix.grid(row=0, column=0, padx=20, pady=20)

# Crear los campos de entrada para la matriz de adyacencia
entry_matrix = []
for i in range(len(adj_matrix)):
    row_entries = []
    for j in range(len(adj_matrix[i])):
        entry = tk.Entry(frame_matrix, width=7, justify="center", font=("Arial", 14))  # Tamaño de fuente aumentado
        entry.insert(0, str(adj_matrix[i][j]))
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
    entry_matrix.append(row_entries)

# Botón para actualizar la matriz de adyacencia y colorear el grafo
update_button = tk.Button(window, text="Actualizar Matriz y Colorear Grafo", command=update_matrix, font=("Arial", 14))
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
