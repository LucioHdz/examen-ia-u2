import math
import heapq
from collections import defaultdict

GRID_PROBLEMA = [
    [0,0,0,1,0],
    [0,1,0,1,0],
    [0,1,0,0,0],
    [0,0,1,1,0],
    [1,0,0,0,0]
]

class Laberinto:
    def __init__(self, grid: list):
        self.filas = len(grid)
        self.cols = len(grid[0])
        self.grid = grid

    @classmethod
    def desde_problema(cls):
        return cls(GRID_PROBLEMA)

    def es_valido(self, r, c):
        return 0 <= r < self.filas and 0 <= c < self.cols and self.grid[r][c] == 0

    def vecinos(self, r, c):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if self.es_valido(r + dr, c + dc)]

    def imprimir(self, camino: list = None, inicio=(0, 0), meta=None):
        meta = meta or (self.filas - 1, self.cols - 1)
        camino_set = set(camino) if camino else set()
        simbolos = {0: ".", 1: "X"}
        print()
        for r in range(self.filas):
            fila = ""
            for c in range(self.cols):
                pos = (r, c)
                if pos == inicio:
                    fila += " S"
                elif pos == meta:
                    fila += " F"
                elif pos in camino_set:
                    fila += " *"
                else:
                    fila += f" {simbolos[self.grid[r][c]]}"
            print(fila)
        print()

def heuristica_manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_estrella(laberinto: Laberinto, inicio, meta):
    open_heap = []
    heapq.heappush(open_heap, (heuristica_manhattan(inicio, meta), 0, inicio))

    g_cost = defaultdict(lambda: math.inf)
    g_cost[inicio] = 0

    padre = {inicio: None}
    visitados = set()

    while open_heap:
        f, g, nodo = heapq.heappop(open_heap)
        if nodo in visitados:
            continue
        visitados.add(nodo)

        if nodo == meta:
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = padre[nodo]
            return camino[::-1]

        for vecino in laberinto.vecinos(*nodo):
            nuevo_g = g + 1
            if nuevo_g < g_cost[vecino]:
                g_cost[vecino] = nuevo_g
                padre[vecino] = nodo
                f_nuevo = nuevo_g + heuristica_manhattan(vecino, meta)
                heapq.heappush(open_heap, (f_nuevo, nuevo_g, vecino))

    return []

def main():
    print("Busqueda A*")
    print("=+" * 20)

    laberinto = Laberinto.desde_problema()
    inicio = (0,0)
    meta = (laberinto.filas - 1, laberinto.cols - 1)

    print(f"\nCuadricula {laberinto.filas}x{laberinto.cols}  S -> Inicio, F -> Meta, X -> Obstaculo")
    laberinto.imprimir(inicio=inicio, meta=meta)

    print("=+" * 20)
    print("A* pura:")
    print("=+" * 20)
    camino = a_estrella(laberinto, inicio, meta)
    if camino:
        print(f"Longitud del camino: {len(camino)} nodos")
        print(f"Costo total: {len(camino) - 1}")
        laberinto.imprimir(camino, inicio, meta)
    else:
        print("Sin solucion :c")


if __name__ == "__main__":
    main()
