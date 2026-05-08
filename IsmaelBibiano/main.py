import math 
import random
import heapq
from collections import defaultdict
    
class Laberinto:
    def __init__(self, filas, columnas, semilla = 42, grid_predefinido = None):
        self.filas = filas
        self.cols = columnas
        if grid_predefinido is not None:
            self.grid = grid_predefinido
        else:
            random.seed(semilla)
            self.grid = self._generar()

    
    def es_valido(self, r, c):
        return (0 <= r < self.filas and
                0 <= c < self.cols and
                self.grid[r][c] == 0)

    def vecinos(self, r, c):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(r+dr, c+dc) for dr, dc in dirs if self.es_valido(r+dr, c+dc)]
    
    def densidad_local(self, r, c, radio = 2):
        total = obstaculos = 0
        for dr in range(-radio, radio+1):
            for dc in range(-radio, radio+1):
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.filas and 0 <= nc < self.cols:
                    total += 1
                    obstaculos += self.grid[nr][nc]
        return obstaculos / total if total else 0.0
    
    def imprimir(self, camino:list = None, inicio = (0,0), meta = None):
        meta = meta or (self.filas-1, self.cols-1)
        camino_set = set(camino) if camino else set()
        simbolos = {0: " · ", 1: " X "}
        print()
        for r in range(self.filas):
            fila = ""
            for c in range(self.cols):
                pos = (r, c)
                if pos == inicio:
                    fila += " S "
                elif pos == meta:
                    fila += " F "
                elif pos in camino_set:
                    fila += " * "
                else:
                    fila += f"{simbolos[self.grid[r][c]]}"
            print(fila)
        print()
    
# Heuristica

def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(laberinto: Laberinto, inicio, meta):
    """
    A* puro con heuristica Manhattan
    """

    def h(nodo):
        return heuristica_manhattan(nodo, meta)
    
    # Creamos una cola de tareas
    open_heap = []
    heapq.heappush(open_heap, (h(inicio), 0, inicio))

    g_cost = defaultdict(lambda: math.inf)
    g_cost[inicio] = 0

    padre = {inicio: None}

    visitados = set()

    # Extraer datos de la lista de tareas que creamos
    while open_heap:
        f, g, nodo = heapq.heappop(open_heap)
        if nodo in visitados:
            continue
        visitados.add(nodo)

        # Si estamos en la meta reconstruimos nuestra meta
        if nodo == meta:
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = padre[nodo]
            # Invertir nuestra salida
            return camino[::-1] # Solucion
        
        # Si no estamos en la meta recorremos nuetsros nodos veicnos
        for vecino in laberinto.vecinos(*nodo):
            nuevo_g = g +1
            if nuevo_g < g_cost[vecino]:
                g_cost[vecino] = nuevo_g
                padre[vecino] = nodo
                h_nuevo = nuevo_g + h(vecino)
                heapq.heappush(open_heap, (h_nuevo, nuevo_g, vecino))
    return [] # sin solución

def main():
    print("="*25)
    print(" Examen U2 - Inteligencia Artificial:")
    print("="*25)

    FILAS, COLS = 5, 5
    laberinto_examen = [
        [0, 0, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0]
    ]
    
    laberinto = Laberinto(FILAS, COLS, grid_predefinido=laberinto_examen)
    inicio = (0,0)
    meta = (FILAS - 1, COLS - 1)

    print(f"\n Laberinto {FILAS} x {COLS} donde S -> Inicio  F -> Meta  X -> Obstaculo")
    laberinto.imprimir(inicio=inicio, meta=meta)

    print("="*25)
    print(" Algoritmo de A*:")
    print("="*25)
    camino_puro = a_estrella(laberinto, inicio, meta)
    if camino_puro:
        print(f"\n Longitud del camino es: {len(camino_puro)} nodos")
        laberinto.imprimir(camino_puro, inicio, meta)
    else:
        print("Sin solución :c")


if __name__ == "__main__":
    main()

