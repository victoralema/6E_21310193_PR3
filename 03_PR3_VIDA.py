import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import networkx as nx

# Función de Dijkstra para calcular las distancias más cortas desde un nodo inicial en un grafo
def dijkstra(graph, start_node):
    distances = {node: float('infinity') for node in graph}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

# Grafo que representa la red de señal Wi-Fi en la casa
graph = {
    'Enrutador': {'A': 3, 'B': 2},
    'A': {'Enrutador': 3, 'C': 4, 'D': 2},
    'B': {'Enrutador': 2, 'C': 1},
    'C': {'A': 4, 'B': 1, 'D': 3},
    'D': {'A': 2, 'C': 3}
}

# Crear una ventana principal de tkinter
root = tk.Tk()
root.title("Dijkstra Algorithm GUI")

# Función para calcular y mostrar las distancias más cortas
def compute_dijkstra():
    start_node = start_node_var.get()
    distances = dijkstra(graph, start_node)
    
    # Mostrar las distancias en una ventana emergente
    result_str = f"Distancias desde el nodo {start_node}:\n"
    for node, distance in distances.items():
        result_str += f"Nodo {node}: Distancia = {distance} (calidad de la señal)\n"
    messagebox.showinfo("Resultado de Dijkstra", result_str)

# Crear y posicionar widgets en la ventana de tkinter
label = ttk.Label(root, text="Selecciona el nodo inicial:")
label.pack(pady=10)

start_node_var = tk.StringVar()
start_node_var.set('Enrutador')  # Valor por defecto

# Dropdown para seleccionar el nodo inicial
start_node_dropdown = ttk.Combobox(root, textvariable=start_node_var, values=list(graph.keys()))
start_node_dropdown.pack(pady=10)

# Botón para calcular las distancias más cortas
compute_button = ttk.Button(root, text="Calcular Distancias", command=compute_dijkstra)
compute_button.pack(pady=10)

# Función para dibujar el grafo usando matplotlib y networkx
def draw_graph():
    G = nx.Graph(graph)
    pos = nx.spring_layout(G)  # Layout para posicionar los nodos
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray')
    plt.title('Red de señal Wi-Fi en la casa')
    
    # Integrar el gráfico en tkinter usando FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Llamar a la función para dibujar el grafo
draw_graph()

# Iniciar el bucle principal de tkinter
root.mainloop()
