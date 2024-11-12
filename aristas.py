"""
Este módulo proporciona una interfaz gráfica utilizando Tkinter para visualizar y colorear las aristas de un grafo.
Utiliza el algoritmo de coloración de aristas basado en el número mínimo de colores necesarios para colorear un grafo
según el grado máximo de sus vértices, conocido como la heurística de Vizing.
El grafo puede ser dirigido o no dirigido y la coloración de las aristas se realiza utilizando una paleta de colores predefinida.
Además, se mide el tiempo de ejecución del algoritmo de coloración para realizar pruebas de rendimiento.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from igraph import Graph, plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time  # Importar el módulo time

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
    Calcula el número mínimo de colores necesarios para colorear las aristas del grafo utilizando el teorema de Vizing.
    
    El número mínimo de colores está basado en el grado máximo de los vértices del grafo. El número mínimo de colores
    necesario será como máximo uno más que el grado máximo del grafo.

    Args:
        graph (Graph): El grafo para el cual se calcula el número mínimo de colores.

    Returns:
        int: El número mínimo de colores necesario para colorear las aristas del grafo.
    """
    max_degree = max(graph.degree())
    return max_degree + 1

def is_safe_edge(edge, color, colors, graph):
    """
    Verifica si es seguro asignar un color a una arista.

    Este método verifica que no haya colisiones de colores con las aristas adyacentes a la arista en cuestión.

    Args:
        edge (Edge): La arista para la cual se está verificando la seguridad del color.
        color (int): El color propuesto para la arista.
        colors (list): La lista de colores de las aristas.
        graph (Graph): El grafo en el cual se realiza la verificación.

    Returns:
        bool: True si el color puede asignarse a la arista, False de lo contrario.
    """
    u = edge.source
    v = edge.target
    for neighbor_edge in graph.es:
        if (neighbor_edge.source == u or neighbor_edge.target == u or 
            neighbor_edge.source == v or neighbor_edge.target == v):
            if colors[neighbor_edge.index] == color:
                return False
    return True

def edge_coloring(graph, num_colors, colors, edge_order):
    """
    Realiza la coloración de las aristas del grafo utilizando un número determinado de colores.

    Asigna un color a cada arista siguiendo el orden de las aristas basado en el grado de los vértices y verifica
    que no haya conflictos en la coloración.

    Args:
        graph (Graph): El grafo a colorear.
        num_colors (int): El número de colores disponibles para la coloración.
        colors (list): Lista que contendrá los colores asignados a cada arista.
        edge_order (list): Lista que define el orden en que se colorean las aristas.

    Returns:
        bool: True si se puede colorear todas las aristas sin conflictos, False de lo contrario.
    """
    for edge_index in edge_order:
        for color in range(num_colors):
            if is_safe_edge(graph.es[edge_index], color, colors, graph):
                colors[edge_index] = color
                break
        else:
            return False
    return True

def graph_coloring(graph, num_colors, colors):
    """
    Colorea las aristas de un grafo utilizando el algoritmo de coloración de aristas.

    El algoritmo asigna colores a las aristas del grafo en función de su grado y el número de colores disponibles.

    Args:
        graph (Graph): El grafo que se va a colorear.
        num_colors (int): El número de colores disponibles para la coloración.
        colors (list): Lista que contendrá los colores asignados a cada arista.

    Returns:
        bool: El resultado de la coloración (True si es posible, False si no lo es).
    """
    edge_order = [index for index in range(len(graph.es))]
    return edge_coloring(graph, num_colors, colors, edge_order)

def measure_execution_time(graph, num_colors):
    """
    Mide el tiempo promedio de ejecución del algoritmo de coloración de aristas para un número de colores determinado.

    Ejecuta el algoritmo 1000 veces y calcula el tiempo promedio de ejecución.

    Args:
        graph (Graph): El grafo sobre el cual se realiza la medición de tiempo.
        num_colors (int): El número de colores utilizados en el algoritmo.

    Returns:
        float: El tiempo promedio de ejecución en segundos.
    """
    colors = [-1] * len(graph.es)  # Asegura que la longitud de colors sea la cantidad de aristas
    times = []
    for _ in range(1000):
        start_time = time.time()
        graph_coloring(graph, num_colors, colors)
        times.append(time.time() - start_time)
    average_time = sum(times) / len(times)
    print(f"Tiempo promedio de ejecucion: {average_time:.6f} segundos")
    return average_time

def update_graph(directed=True):
    """
    Actualiza la visualización del grafo con los colores de las aristas basados en el algoritmo de coloración.

    Dependiendo del valor de la variable `directed`, se genera una visualización del grafo dirigido o no dirigido.

    Args:
        directed (bool): Determina si el grafo es dirigido (True) o no dirigido (False).
    """
    global adj_matrix
    g = Graph.Adjacency(adj_matrix)
    if not directed:
        g.to_undirected()

    required_colors = min_colors_vizing(g)
    num_colors = max(required_colors, len(palette))

    avg_time = measure_execution_time(g, num_colors)
    print(f"Tiempo promedio de ejecucion: {avg_time:.6f} segundos")

    edge_degrees = [(edge.index, g.degree(edge.source) + g.degree(edge.target)) for edge in g.es]
    edge_order = [index for index, degree in sorted(edge_degrees, key=lambda x: -x[1])]
    
    colors = [-1] * len(g.es)
    
    if edge_coloring(g, num_colors, colors, edge_order):
        g.es["color"] = [palette[color % len(palette)] for color in colors]
        fig, ax = plt.subplots(figsize=(7, 7))
        plot(g, target=ax, vertex_size=40, vertex_color='lightblue', vertex_label=range(len(g.vs)),
             edge_width=2, edge_color=g.es["color"])
        ax.set_title("Coloración de las Aristas del Grafo (" + ("Dirigido" if directed else "No Dirigido") + ")")
        
        for widget in frame_graph.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", f"No es posible colorear las aristas del grafo con {num_colors} colores.")

def update_matrix():
    """
    Actualiza la matriz de adyacencia con los valores proporcionados por el usuario.

    Valida que los valores ingresados sean 0 o 1, y luego actualiza la matriz de adyacencia. Después, actualiza la
    visualización del grafo con la nueva matriz.

    Si los valores ingresados no son válidos, se muestra un mensaje de error.
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

# Configuración de la ventana principal y la interfaz gráfica
window = tk.Tk()
window.title("Coloración de Aristas de Grafo - GUI Mejorada")
window.geometry("1000x800")

frame_matrix = tk.LabelFrame(window, text="Matriz de Adyacencia", padx=10, pady=10)
frame_matrix.grid(row=0, column=0, padx=20, pady=20)

entry_matrix = []
for i in range(len(adj_matrix)):
    row_entries = []
    for j in range(len(adj_matrix[i])):
        entry = tk.Entry(frame_matrix, width=3, justify="center")
        entry.insert(0, str(adj_matrix[i][j]))
        entry.grid(row=i, column=j)
        row_entries.append(entry)
    entry_matrix.append(row_entries)

update_button = tk.Button(window, text="Actualizar Matriz", command=update_matrix)
update_button.grid(row=1, column=0, padx=20, pady=10)

frame_graph = tk.Frame(window)
frame_graph.grid(row=0, column=1, rowspan=2, padx=20, pady=20)

directed_var = tk.BooleanVar(value=True)
directed_checkbox = tk.Checkbutton(window, text="Grafo Dirigido", variable=directed_var)
directed_checkbox.grid(row=2, column=0, padx=20, pady=10)

update_graph_button = tk.Button(window, text="Actualizar Grafo", command=lambda: update_graph(directed_var.get()))
update_graph_button.grid(row=2, column=1, padx=20, pady=10)

window.mainloop()
