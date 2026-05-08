import math
import random 
import heapq 
from collections import defaultdict

class Laberinto:
    def __init__(self, filas, cols, semilla = 42):
        self.filas = filas
        self.cols = cols
        random.seed(semilla)
        self.grid = [
            [0, 0, 0, 1, 0], 
            [0, 1, 0, 0, 0], 
            [0, 1, 0, 0, 0], 
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0]
        ]
    
    def es_valido(self, r, c): # validar que no se salga de estos parametros
        return (
            0 <= r < self.filas and 
            0 <= c < self.cols and
            self.grid[r][c] == 0
        )
    
    def vecinos(self, r, c): # conocer el entorno (abajo, arriba, izquierda, derecha)
        dirs = [(-1,0),(1,0),(0,-1),(0,1)] # definir tuplas de 4 por que nos estamos moviendo en 2D
        return [(r + dr, c + dc) for dr, dc in dirs if self.es_valido(r + dr, c + dc)] # tupla de nuestra direccion que tenemos

    def imprimir(self, camino:list = None, inicio = (0,0), meta = None):
        meta = meta or (self.filas - 1, self.cols - 1) 
        camino_set = set(camino) if camino else set() # definir nuestro camino
        simbolos = {0: "·", 1: "X"} # laberinto
        print()
        for r in range(self.filas): # recorrer grid completamente
            fila = ""
            for c in range(self.cols):
                pos = (r,c)
                if pos == inicio:
                    fila += " S"
                elif pos == meta:
                    fila += " F"
                elif pos in camino_set: # camino_set es el que se va recorriendo
                    fila += " *"
                else:
                    fila += f" {simbolos[self.grid[r][c]]}" # template string formatear
            print(fila)
        print()

# Heuristica 
def heuristica_manhattan(a, b): # arreglo-tupla de 2 elementos
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # abs para que frene

# estudiar esto 
def a_estrella(laberinto:Laberinto, inicio, meta):
    """
    A* puro usando únicamente heurística de Manhattan
    """
    def h(nodo):
        return heuristica_manhattan(nodo, meta) 

    open_heap = []
    # cola primero en entrar primero en salir (usada como prioridad)
    heapq.heappush(open_heap, (h(inicio), 0, inicio)) # cola de tareas
       
    # calcular un costo
    g_cost = defaultdict(lambda:math.inf) 
    g_cost[inicio] = 0 
    padre = {inicio:None} # vamos a empezar nuestro recorrido en la lista
    visitados = set()

    while open_heap:
        f, g, nodo = heapq.heappop(open_heap) # los estamos extrayendo de la tupla de la cola de tareas
        if nodo in visitados:
            continue
        visitados.add(nodo) # lugares-posiciones ya recorridas

        if nodo == meta:
            # reconstruir nuestro camino
            camino = []
            while nodo is not None: # vamos a empezar a recorrer hasta que no empecemos con un None
                camino.append(nodo) # agregado el nodo
                nodo = padre[nodo] # registrando del final hacia el inicio
            return camino[::-1] # invertir nodo en vez de final - inicio lo hara inicio - final {**solucion**}
        
        for vecino in laberinto.vecinos(*nodo):
            nuevo_g = g + 1
            if nuevo_g < g_cost[vecino]:
                g_cost[vecino] = nuevo_g
                padre[vecino] = nodo
                h_nuevo = nuevo_g + h(vecino) # h funcion de heuristica
                heapq.heappush(open_heap, (h_nuevo, nuevo_g, vecino)) # pasamos nueva tupla
    return [] # vamos a tener algo que {**no tiene solucion**}

def main():
    print("Busqueda A*")
    print("="*20)
    FILAS, COLS = 5, 5
    laberinto = Laberinto(FILAS, COLS)  
    inicio = (0, 0)
    meta = (FILAS - 1, COLS - 1)
    
    print(f"\n Laberinto {FILAS}x{COLS}  S -> Inicio {inicio} -> Meta {meta} -> Obstaculo ")
    laberinto.imprimir(inicio, meta = meta)

    print("="*20)
    print("Ejecutando A*:")
    print("="*20)
    
    camino = a_estrella(laberinto, inicio, meta)
    
    if camino:
        print(f"Costo es del: {len(camino)} nodos")
        laberinto.imprimir(camino, inicio, meta)
    else:
        print("Sin solucion :C")

if __name__ == "__main__":
    main()
