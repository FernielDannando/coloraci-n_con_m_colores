"""
Módulo de Coloración de Grafos con Interfaz Gráfica

Este módulo implementa una aplicación GUI en Tkinter que permite a los usuarios visualizar y colorear un grafo
según una matriz de adyacencia dada, utilizando un número limitado de colores. La coloración del grafo asegura que
nodos adyacentes no tengan el mismo color, y el módulo utiliza un algoritmo de backtracking para asignar los colores
a cada nodo. Además, permite a los usuarios medir el tiempo de ejecución promedio del algoritmo de coloración.

Clases y funciones principales:

- `is_safe(node, color, colors, graph)`: Verifica si es seguro asignar un color específico a un nodo, asegurando que
  ningún nodo adyacente tenga el mismo color.

- `graph_coloring(graph, num_colors, colors, node=0)`: Implementa el algoritmo de backtracking para colorear el grafo,
  asignando colores a cada nodo sin que nodos adyacentes compartan el mismo color.

- `measure_execution_time(graph, num_colors)`: Calcula el tiempo promedio de ejecución del algoritmo de coloración de grafos
  en función de múltiples iteraciones, brindando información sobre el rendimiento.

- `update_graph(directed=True)`: Actualiza y muestra la visualización del grafo en la interfaz, coloreando los nodos
  según la matriz de adyacencia y el número de colores disponibles. Los nodos pueden ser mostrados en grafos dirigidos o no dirigidos.

- `update_matrix()`: Actualiza la matriz de adyacencia a partir de los valores ingresados en la interfaz y luego refresca
  la visualización del grafo con los nuevos valores de la matriz.

Dependencias:
- `igraph`: Utilizado para representar y visualizar grafos.
- `matplotlib`: Utilizado para la visualización gráfica de los nodos y bordes del grafo en la GUI.
- `tkinter`: Biblioteca para la creación de la interfaz de usuario.
"""
import time
import tkinter as tk
from tkinter import messagebox, ttk
from igraph import Graph, plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    Verifies if it's safe to assign a color to a given node, ensuring that no adjacent node has the same color.

    Args:
        node (int): Index of the node to color.
        color (int): Color to assign to the node.
        colors (list): List of colors assigned to each node.
        graph (igraph.Graph): Graph object containing nodes and edges.

    Returns:
        bool: True if it's safe to assign the color, False otherwise.
    """
    for neighbor in graph.neighbors(node):
        if colors[neighbor] == color:
            return False
    return True

def graph_coloring(graph, num_colors, colors, node=0):
    """
    Backtracking algorithm to color a graph, assigning colors to each node such that adjacent nodes do not share the same color.

    Args:
        graph (igraph.Graph): Graph object containing nodes and edges.
        num_colors (int): Number of colors available for coloring.
        colors (list): List of colors assigned to each node.
        node (int): Current node to be colored (default is 0).

    Returns:
        bool: True if the graph can be colored with the given number of colors, False otherwise.
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

def measure_execution_time(graph, num_colors):
    """
    Measures the average execution time of the graph coloring algorithm.

    Args:
        graph (igraph.Graph): Graph object containing nodes and edges.
        num_colors (int): Number of colors available for coloring.

    Prints:
        str: Average execution time of the algorithm in seconds.
    """
    colors = [-1] * len(graph.vs)
    times = []
    for _ in range(1000):
        start_time = time.time()
        graph_coloring(graph, num_colors, colors)
        times.append(time.time() - start_time)
    average_time = sum(times) / len(times)
    print(f"Tiempo promedio de ejecucion: {average_time:.6f} segundos")

def update_graph(directed=True):
    """
    Updates the graph visualization in the GUI, coloring nodes based on the adjacency matrix and the available colors.

    Args:
        directed (bool): Whether the graph is directed or undirected. Default is True.

    Modifies:
        frame_graph (tk.Frame): Frame in the GUI where the graph is displayed.

    Raises:
        messagebox.showerror: If the graph cannot be colored with the available number of colors.
    """
    global adj_matrix
    g = Graph.Adjacency(adj_matrix)
    if not directed:
        g.to_undirected()
    colors = [-1] * len(g.vs)
    
    measure_execution_time(g, num_colors)
    
    if graph_coloring(g, num_colors, colors):
        g.vs["color"] = [palette[color % num_colors] for color in colors]
        fig, ax = plt.subplots(figsize=(7, 7))
        plot(g, target=ax, vertex_size=40, vertex_color=g.vs["color"], vertex_label=range(len(g.vs)),
             edge_width=0.8, edge_color='gray')
        ax.set_title("Coloración del Grafo (" + ("Dirigido" if directed else "No Dirigido") + ")")
        
        for widget in frame_graph.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", f"No es posible colorear el grafo con {num_colors} colores.")

def update_matrix():
    """
    Updates the adjacency matrix based on values entered in the GUI and then updates the graph visualization based on the new matrix.

    Modifies:
        adj_matrix (list): Updates the global adjacency matrix with new values entered by the user.

    Raises:
        messagebox.showerror: If invalid input values are entered (not 0 or 1).
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

window = tk.Tk()
window.title("Coloración de nodos de un Grafo")
window.geometry("1000x800")

frame_matrix = tk.LabelFrame(window, text="Matriz de Adyacencia", padx=10, pady=10)
frame_matrix.grid(row=0, column=0, padx=20, pady=20)

entry_matrix = []
for i in range(len(adj_matrix)):
    row_entries = []
    for j in range(len(adj_matrix[i])):
        entry = tk.Entry(frame_matrix, width=7, justify="center", font=("Arial", 14))
        entry.insert(0, str(adj_matrix[i][j]))
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
    entry_matrix.append(row_entries)

update_button = tk.Button(window, text="Actualizar Matriz y Colorear Grafo", command=update_matrix, font=("Arial", 14))
update_button.grid(row=1, column=0, pady=20)

frame_graph = tk.LabelFrame(window, text="Visualización del Grafo", padx=10, pady=10)
frame_graph.grid(row=0, column=1, rowspan=2, padx=20, pady=20)

directed_button = tk.Button(window, text="Mostrar Grafo Dirigido", command=lambda: update_graph(directed=True), font=("Arial", 12))
directed_button.grid(row=2, column=0, pady=10)

undirected_button = tk.Button(window, text="Mostrar Grafo No Dirigido", command=lambda: update_graph(directed=False), font=("Arial", 12))
undirected_button.grid(row=3, column=0, pady=10)

update_graph()

window.mainloop()
