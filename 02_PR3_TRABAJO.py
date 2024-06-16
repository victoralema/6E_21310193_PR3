#Victor Eduardo Aleman Padilla 21310193

import heapq  # Importa el módulo heapq para usar colas de prioridad
import tkinter as tk  # Importa tkinter, la biblioteca estándar de GUI de Python
from tkinter import messagebox, scrolledtext  # Importa clases específicas de tkinter

# Definición de la función dijkstra para buscar la ruta más directa
def dijkstra(almacen, inicio, fin, paso_a_paso):
    # Tamaño de la matriz de almacenamiento
    filas = len(almacen)
    columnas = len(almacen[0])
    
    # Matriz para almacenar el número mínimo de movimientos para llegar a cada punto
    movimientos = [[float('inf')] * columnas for _ in range(filas)]
    movimientos[inicio[0]][inicio[1]] = 0  # Inicializa el punto de inicio con 0 movimientos
    pq = [(0, inicio)]  # Cola de prioridad para realizar el algoritmo de Dijkstra
    anteriores = [[None] * columnas for _ in range(filas)]  # Matriz para almacenar los puntos anteriores
    
    # Direcciones posibles (horizontal, vertical y diagonales)
    direcciones = [
        (0, 1), (1, 0), (0, -1), (-1, 0),    # derecha, abajo, izquierda, arriba
        (1, 1), (-1, 1), (1, -1), (-1, -1)  # diagonales
    ]
    
    while pq:
        mov_actual, (x, y) = heapq.heappop(pq)  # Extrae el punto con menor número de movimientos
        
        if (x, y) == fin:  # Si alcanzamos el punto final, termina el algoritmo
            break
        
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if mov_actual + 1 < movimientos[nx][ny]:  # Si encontramos una ruta más corta
                    movimientos[nx][ny] = mov_actual + 1  # Actualiza el número de movimientos
                    anteriores[nx][ny] = (x, y)  # Registra el punto anterior
                    heapq.heappush(pq, (mov_actual + 1, (nx, ny)))  # Agrega el punto a la cola de prioridad
                    # Registro del paso en el cuadro de texto paso_a_paso
                    paso_a_paso.insert(tk.END, f"Desde ({x}, {y}) a ({nx}, {ny})\n")
                    paso_a_paso.see(tk.END)  # Hacer scroll hasta el final
    
    # Reconstruye la ruta mínima encontrada desde el punto final al inicial
    ruta = []
    nodo_actual = fin
    while nodo_actual is not None:
        ruta.append(nodo_actual)
        nodo_actual = anteriores[nodo_actual[0]][nodo_actual[1]]
    ruta.reverse()  # Invierte la lista para obtener la ruta desde el inicio al final
    
    return movimientos[fin[0]][fin[1]], ruta

# Definición de la clase DijkstraSimulator para la interfaz gráfica
class DijkstraSimulator(tk.Tk):
    def __init__(self, almacen):
        super().__init__()  # Inicializa la clase base (tk.Tk)
        self.title("Simulador de Dijkstra")  # Configura el título de la ventana principal
        self.almacen = almacen  # Almacena la matriz de almacenamiento
        self.matriz_labels = []  # Lista para almacenar etiquetas de la matriz
        self.paso_a_paso = None  # Inicializa la variable para el cuadro de texto de paso a paso
        self.puntos = []  # Lista para almacenar los puntos seleccionados
        
        self.inicializar_gui()  # Llama al método para inicializar la interfaz gráfica
    
    def inicializar_gui(self):
        # Crear cuadro de texto de paso a paso con scroll
        self.paso_a_paso = scrolledtext.ScrolledText(self, width=30, height=10, wrap=tk.WORD)
        self.paso_a_paso.grid(row=1, column=7, rowspan=7, padx=10, pady=10)  # Ubica el cuadro de texto en la interfaz
        
        # Crear etiquetas de columna
        for j in range(len(self.almacen[0])):
            label = tk.Label(self, text=f"Col {j}", borderwidth=1, relief="solid", width=5, height=2)
            label.grid(row=0, column=j+1)  # Ubica la etiqueta en la interfaz
        
        # Crear etiquetas de fila y de la matriz
        for i in range(len(self.almacen)):
            fila_labels = []
            label = tk.Label(self, text=f"Fila {i}", borderwidth=1, relief="solid", width=5, height=2)
            label.grid(row=i+1, column=0)  # Ubica la etiqueta de fila en la interfaz
            for j in range(len(self.almacen[0])):
                label = tk.Label(self, text=str(self.almacen[i][j]), borderwidth=1, relief="solid", width=5, height=2)
                label.grid(row=i+1, column=j+1)  # Ubica la etiqueta de la celda en la interfaz
                label.bind("<Button-1>", lambda e, x=i, y=j: self.agregar_punto(x, y))  # Asocia un evento a cada etiqueta
                fila_labels.append(label)
            self.matriz_labels.append(fila_labels)  # Agrega la fila de etiquetas a la matriz de etiquetas
        
        # Botón para buscar la ruta mínima
        self.boton_buscar_ruta = tk.Button(self, text="Buscar Ruta", command=self.buscar_ruta)
        self.boton_buscar_ruta.grid(row=7, column=0, columnspan=5)  # Ubica el botón en la interfaz
        
        # Botón para reiniciar selecciones
        self.boton_reiniciar = tk.Button(self, text="Reiniciar Selecciones", command=self.reiniciar_selecciones)
        self.boton_reiniciar.grid(row=8, column=0, columnspan=5)  # Ubica el botón en la interfaz
    
    def agregar_punto(self, x, y):
        self.puntos.append((x, y))  # Agrega el punto seleccionado a la lista de puntos
        self.matriz_labels[x][y].config(bg="yellow")  # Cambia el color de fondo de la etiqueta a amarillo
        messagebox.showinfo("Punto Agregado", f"Punto agregado en ({x}, {y})")  # Muestra un mensaje informativo
    
    def buscar_ruta(self):
        if len(self.puntos) < 2:  # Verifica que haya al menos dos puntos seleccionados
            messagebox.showwarning("Advertencia", "Debe agregar al menos dos puntos")
            return
        
        self.paso_a_paso.delete('1.0', tk.END)  # Limpia el cuadro de texto de paso a paso
        
        movimientos_totales = 0  # Inicializa el contador de movimientos totales
        ruta_total = []  # Lista para almacenar la ruta total
        
        for i in range(len(self.puntos) - 1):
            inicio = self.puntos[i]  # Punto de inicio de la ruta actual
            fin = self.puntos[i + 1]  # Punto final de la ruta actual
            movimientos, ruta = dijkstra(self.almacen, inicio, fin, self.paso_a_paso)  # Ejecuta Dijkstra
            movimientos_totales += movimientos  # Suma los movimientos mínimos
            if i > 0:
                ruta = ruta[1:]  # Evita duplicar los puntos de conexión
            ruta_total.extend(ruta)  # Agrega la ruta actual a la ruta total
        
        messagebox.showinfo("Ruta Encontrada", f"El número mínimo de movimientos es {movimientos_totales}")
        self.mostrar_ruta(ruta_total)  # Muestra la ruta mínima en la interfaz gráfica
    
    def mostrar_ruta(self, ruta):
        for i in range(len(self.almacen)):
            for j in range(len(self.almacen[0])):
                self.matriz_labels[i][j].config(bg="white")  # Restablece el color de fondo de todas las etiquetas
        
        for (x, y) in ruta:
            self.matriz_labels[x][y].config(bg="lightblue")  # Cambia el color de fondo de las etiquetas de la ruta a azul claro
    
        for (x, y) in self.puntos:
            self.matriz_labels[x][y].config(bg="yellow")  # Mantén el color de fondo de las etiquetas de puntos seleccionados
    
    def reiniciar_selecciones(self):
        self.puntos = []  # Reinicia la lista de puntos seleccionados
        self.paso_a_paso.delete('1.0', tk.END)  # Limpia el cuadro de texto de paso a paso
        for i in range(len(self.almacen)):
            for j in range(len(self.almacen[0])):
                self.matriz_labels[i][j].config(bg="white")  # Restablece el color de fondo de todas las etiquetas

# Programa principal
if __name__ == "__main__":
    # Matriz de almacenamiento para el simulador
    almacen = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
        [5, 6, 7, 8, 9],
        [6, 7, 8, 9, 10]
    ]
    
    # Crear una instancia de la aplicación DijkstraSimulator
    app = DijkstraSimulator(almacen)
    app.mainloop()  # Ejecutar el loop principal de la interfaz gráfica
