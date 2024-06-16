#Victor Eduardo Aleman Padilla 21310193

import tkinter as tk  # Importamos la biblioteca tkinter para la interfaz gráfica
from tkinter import messagebox  # Importamos messagebox de tkinter para mostrar mensajes emergentes

class TransportRoutePlanner:
    def __init__(self, master):
        self.master = master  # Guardamos una referencia al objeto raíz de la ventana
        self.master.title("Planificador de Rutas de Transporte")  # Establecemos el título de la ventana
        
        self.canvas = tk.Canvas(self.master, width=600, height=500)  # Creamos un canvas dentro de la ventana
        self.canvas.pack()  # Empaquetamos el canvas dentro de la ventana
        
        # Definimos el grafo que representa las paradas y rutas de autobús
        self.graph = {
            'A': {'B': 10, 'C': 5, 'E': 20},
            'B': {'A': 10, 'D': 15},
            'C': {'A': 5, 'D': 20},
            'D': {'B': 15, 'C': 20, 'F': 10},
            'E': {'A': 20, 'F': 5, 'G': 15},
            'F': {'D': 10, 'E': 5, 'H': 8},
            'G': {'E': 15, 'H': 12, 'I': 7},
            'H': {'F': 8, 'G': 12, 'I': 5},
            'I': {'G': 7, 'H': 5}
        }
        
        # Diccionario para almacenar los colores de las aristas del grafo
        self.edge_colors = {
            ('A', 'B'): 'gray',
            ('A', 'C'): 'gray',
            ('A', 'E'): 'gray',
            ('B', 'A'): 'gray',
            ('B', 'D'): 'gray',
            ('C', 'A'): 'gray',
            ('C', 'D'): 'gray',
            ('D', 'B'): 'gray',
            ('D', 'C'): 'gray',
            ('D', 'F'): 'gray',
            ('E', 'A'): 'gray',
            ('E', 'F'): 'gray',
            ('E', 'G'): 'gray',
            ('F', 'D'): 'gray',
            ('F', 'E'): 'gray',
            ('F', 'H'): 'gray',
            ('G', 'E'): 'gray',
            ('G', 'H'): 'gray',
            ('G', 'I'): 'gray',
            ('H', 'F'): 'gray',
            ('H', 'G'): 'gray',
            ('H', 'I'): 'gray',
            ('I', 'G'): 'gray',
            ('I', 'H'): 'gray',
        }
        
        self.draw_graph()  # Llamamos al método para dibujar el grafo en el canvas
        
        self.start_node = tk.StringVar()  # Variable para almacenar la parada de origen seleccionada
        self.end_node = tk.StringVar()  # Variable para almacenar la parada de destino seleccionada
        
        # Creación de etiquetas y menús desplegables para seleccionar origen y destino
        tk.Label(self.master, text="Seleccione la parada de origen:").pack()
        tk.OptionMenu(self.master, self.start_node, *list(self.graph.keys())).pack()
        
        tk.Label(self.master, text="Seleccione la parada de destino:").pack()
        tk.OptionMenu(self.master, self.end_node, *list(self.graph.keys())).pack()
        
        # Botón para calcular la ruta más corta
        tk.Button(self.master, text="Calcular Ruta", command=self.calculate_route).pack()

    def draw_graph(self):
        # Posiciones de los nodos en el canvas
        node_positions = {
            'A': (100, 100),
            'B': (200, 100),
            'C': (200, 200),
            'D': (300, 150),
            'E': (100, 200),
            'F': (300, 200),
            'G': (150, 300),
            'H': (250, 300),
            'I': (200, 400)
        }
        
        # Dibujamos los nodos como óvalos y etiquetas de texto en el canvas
        for node, pos in node_positions.items():
            self.canvas.create_oval(pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10, fill='white', outline='black')
            self.canvas.create_text(pos[0], pos[1], text=node)
        
        # Dibujamos las aristas del grafo en el canvas
        for node, neighbors in self.graph.items():
            x1, y1 = node_positions[node]
            for neighbor, weight in neighbors.items():
                x2, y2 = node_positions[neighbor]
                color = self.edge_colors.get((node, neighbor), 'gray')  # Obtenemos el color de la arista
                self.canvas.create_line(x1, y1, x2, y2, fill=color)  # Dibujamos la arista con el color correspondiente

    def calculate_route(self):
        self.reset_edge_colors()  # Llamamos al método para reiniciar los colores de las aristas
        start = self.start_node.get()  # Obtenemos la parada de origen seleccionada
        end = self.end_node.get()  # Obtenemos la parada de destino seleccionada
        
        shortest_distances = self.dijkstra(start)  # Calculamos las distancias más cortas desde el nodo de origen
        shortest_path = self.get_shortest_path(start, end, shortest_distances)  # Obtenemos la ruta más corta
        
        self.highlight_shortest_path(shortest_path)  # Resaltamos la ruta más corta en el grafo
        messagebox.showinfo("Ruta más corta", f"La ruta más corta de {start} a {end} es: {shortest_path}")  # Mostramos un mensaje con la ruta más corta

    def dijkstra(self, start):
        distances = {node: float('infinity') for node in self.graph}  # Inicializamos las distancias con infinito
        distances[start] = 0  # La distancia al nodo de inicio es 0
        unvisited = set(self.graph.keys())  # Conjunto de nodos no visitados
        
        while unvisited:
            current_node = min(unvisited, key=lambda node: distances[node])  # Seleccionamos el nodo no visitado con la menor distancia
            unvisited.remove(current_node)  # Removemos el nodo actual del conjunto de no visitados
            
            # Actualizamos las distancias de los vecinos del nodo actual
            for neighbor, weight in self.graph[current_node].items():
                distance = distances[current_node] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance  # Actualizamos la distancia más corta al vecino
        
        return distances  # Retornamos las distancias más cortas desde el nodo de inicio

    def get_shortest_path(self, start, end, distances):
        path = []  # Lista para almacenar la ruta más corta
        current_node = end  # Empezamos desde el nodo de destino
        
        while current_node != start:
            path.append(current_node)  # Añadimos el nodo actual a la ruta
            # Buscamos el vecino que lleva al nodo actual según las distancias más cortas
            for neighbor, weight in self.graph[current_node].items():
                if distances[current_node] == distances[neighbor] + weight:
                    current_node = neighbor  # Movemos al nodo vecino
                    break
        
        path.append(start)  # Añadimos el nodo de inicio a la ruta
        path.reverse()  # Revertimos la lista para obtener la ruta correcta
        return path  # Retornamos la ruta más corta como una lista de nodos

    def highlight_shortest_path(self, path):
        for i in range(len(path) - 1):
            node1 = path[i]  # Nodo inicial de la arista
            node2 = path[i + 1]  # Nodo final de la arista
            self.edge_colors[(node1, node2)] = 'green'  # Cambiamos el color de la arista a verde
            self.edge_colors[(node2, node1)] = 'green'  # Cambiamos el color de la arista inversa a verde
            self.draw_graph()  # Redibujamos el grafo con los nuevos colores
            self.master.update()  # Actualizamos la ventana
            self.master.after(1000)  # Pausa de 1 segundo entre iteraciones

    def reset_edge_colors(self):
        # Reiniciamos todos los colores de las aristas a 'gray' (gris)
        for edge in self.edge_colors:
            self.edge_colors[edge] = 'gray'
        self.draw_graph()  # Redibujamos el grafo con los colores reiniciados

def main():
    root = tk.Tk()  # Creamos la ventana principal de tkinter
    app = TransportRoutePlanner(root)  # Creamos una instancia de la aplicación de planificación de rutas
    root.mainloop()  # Iniciamos el bucle principal de la interfaz gráfica

if __name__ == "__main__":
    main()  # Llamamos a la función principal para iniciar la aplicación
