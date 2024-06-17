import tkinter as tk  # Importa el módulo tkinter y lo alias como tk
from tkinter import ttk  # Importa el submódulo ttk desde tkinter para widgets temáticos
from tkinter import messagebox  # Importa el submódulo messagebox desde tkinter para mostrar mensajes de diálogo
import heapq  # Importa el módulo heapq para utilizar colas de prioridad (heap)

class DijkstraGUI:
    def __init__(self, master):
        self.master = master  # Guarda la referencia a la ventana principal (root) en self.master
        self.master.title("Simulador de Dijkstra")  # Establece el título de la ventana principal
        
        # Definición del grafo como un diccionario de diccionarios con pesos entre nodos
        self.graph = {
            'Trabajo': {'Casa': 1, 'Ceti': 4},
            'Casa': {'Trabajo': 1, 'Ceti': 2, 'Servicio': 5},
            'Ceti': {'Trabajo': 4, 'Casa': 2, 'Servicio': 1},
            'Servicio': {'Casa': 5, 'Ceti': 1}
        }
        
        # Creación de etiquetas y cuadros combinados (combobox) para seleccionar nodos de inicio y destino
        self.label_start = ttk.Label(master, text="Nodo de inicio:")  # Crea una etiqueta con texto
        self.label_start.grid(row=0, column=0, padx=10, pady=10)  # Coloca la etiqueta en la cuadrícula de la ventana
        
        self.start_var = tk.StringVar()  # Variable de control para el cuadro combinado de inicio
        self.start_combo = ttk.Combobox(master, textvariable=self.start_var, values=list(self.graph.keys()))
        # Crea un cuadro combinado con valores iniciales y asigna la variable de control
        self.start_combo.grid(row=0, column=1, padx=10, pady=10)  # Coloca el cuadro combinado en la cuadrícula
        
        # Define el evento de selección del cuadro de inicio para actualizar las opciones del cuadro de destino
        self.start_combo.bind('<<ComboboxSelected>>', self.update_end_options)
        
        # Creación de etiqueta y cuadro combinado para seleccionar nodo de destino
        self.label_end = ttk.Label(master, text="Nodo de destino:")
        self.label_end.grid(row=1, column=0, padx=10, pady=10)
        
        self.end_var = tk.StringVar()  # Variable de control para el cuadro combinado de destino
        self.end_combo = ttk.Combobox(master, textvariable=self.end_var, values=list(self.graph.keys()))
        # Crea un cuadro combinado con valores iniciales y asigna la variable de control
        self.end_combo.grid(row=1, column=1, padx=10, pady=10)  # Coloca el cuadro combinado en la cuadrícula
        
        # Etiqueta para mostrar el resultado del cálculo
        self.label_output = ttk.Label(master, text="Resultado:")
        self.label_output.grid(row=2, column=0, padx=10, pady=10)
        
        # Cuadro de texto para mostrar el resultado del cálculo
        self.output_text = tk.Text(master, height=6, width=30)
        self.output_text.grid(row=2, column=1, padx=10, pady=10)
        
        # Botón para iniciar el cálculo del camino más corto usando Dijkstra
        self.run_button = ttk.Button(master, text="Calcular Ruta", command=self.calculate_shortest_path)
        self.run_button.grid(row=3, columnspan=2, padx=10, pady=10)
        
    def update_end_options(self, event):
        # Método para actualizar las opciones del cuadro combinado de destino al seleccionar un inicio
        selected_start = self.start_var.get()  # Obtiene el nodo de inicio seleccionado
        valid_ends = list(self.graph[selected_start].keys())  # Obtiene los nodos válidos como destinos
        self.end_combo['values'] = valid_ends  # Actualiza los valores del cuadro combinado de destino
        self.end_var.set(valid_ends[0] if valid_ends else "")  # Establece el primer valor como selección inicial
        
    def calculate_shortest_path(self):
        # Método para calcular y mostrar el camino más corto entre el nodo de inicio y el nodo de destino
        start_node = self.start_var.get()  # Obtiene el nodo de inicio seleccionado
        end_node = self.end_var.get()  # Obtiene el nodo de destino seleccionado
        
        # Verifica si el nodo de inicio no está en el grafo
        if start_node not in self.graph:
            messagebox.showerror("Error", f"El nodo {start_node} no existe en el grafo.")
            return
        
        # Verifica si el nodo de destino no está en el grafo
        if end_node not in self.graph:
            messagebox.showerror("Error", f"El nodo {end_node} no existe en el grafo.")
            return
        
        # Ejecuta el algoritmo de Dijkstra para encontrar la distancia más corta y el camino más corto
        shortest_distances, shortest_path = self.dijkstra(self.graph, start_node, end_node)
        shortest_distance = shortest_distances[end_node]  # Obtiene la distancia más corta al nodo de destino
        
        # Borra el contenido anterior del cuadro de texto de salida
        self.output_text.delete(1.0, tk.END)
        
        # Muestra el resultado en el cuadro de texto de salida
        if shortest_distance == float('inf'):
            self.output_text.insert(tk.END, f"No hay ruta desde {start_node} a {end_node}.\n")
        else:
            self.output_text.insert(tk.END, f"Distancia más corta desde {start_node} a {end_node}: {shortest_distance}\n")
            self.output_text.insert(tk.END, "Ruta:\n")
            for step in shortest_path:
                self.output_text.insert(tk.END, f"{step}\n")
    
    def dijkstra(self, graph, start, end):
        # Implementación del algoritmo de Dijkstra para encontrar la distancia más corta y el camino más corto
        distances = {node: float('inf') for node in graph}  # Inicializa todas las distancias como infinito
        distances[start] = 0  # La distancia al nodo de inicio es 0
        priority_queue = [(0, start)]  # Cola de prioridad con tuplas (distancia, nodo)
        path = {start: []}  # Diccionario para almacenar el camino más corto hasta cada nodo
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)  # Extrae el nodo con menor distancia
            
            if current_node == end:  # Si llegamos al nodo de destino, terminamos
                break
            
            if current_distance > distances[current_node]:  # Si la distancia actual es mayor, continuamos
                continue
            
            for neighbor, weight in graph[current_node].items():  # Itera sobre los vecinos del nodo actual
                distance = current_distance + weight  # Calcula la distancia al vecino
                
                if distance < distances[neighbor]:  # Si encontramos una distancia más corta al vecino
                    distances[neighbor] = distance  # Actualiza la distancia más corta
                    path[neighbor] = path[current_node] + [neighbor]  # Actualiza el camino más corto
                    heapq.heappush(priority_queue, (distance, neighbor))  # Agrega a la cola de prioridad
        
        shortest_path = path[end] if end in path else []  # Obtiene el camino más corto hasta el nodo de destino
        return distances, shortest_path  # Retorna las distancias más cortas y el camino más corto

def main():
    root = tk.Tk()  # Crea la ventana principal
    dijkstra_gui = DijkstraGUI(root)  # Crea una instancia de la interfaz gráfica
    root.mainloop()  # Inicia el bucle principal de eventos

if __name__ == "__main__":
    main()  # Ejecuta la función main si este script es el programa principal
