import math
import heapq
from collections import defaultdict


class Laberinto:
    def __init__(self):
        self.grid = [
            [0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0],
        ]

        self.filas = 5
        self.cols = 5

    def es_valido(self, r, c):
        return 0 <= r < self.filas and 0 <= c < self.cols and self.grid[r][c] == 0

    def vecinos(self, r, c):
        dirs = [
            (-1, 0),  # arriba
            (1, 0),   # abajo
            (0, -1),  # izquierda
            (0, 1),   # derecha
        ]

        return [(r + dr, c + dc) for dr, dc in dirs if self.es_valido(r + dr, c + dc)]

    def imprimir(self, camino=None, inicio=(0, 0), meta=None):
        meta = meta or (self.filas - 1, self.cols - 1)
        camino_set = set(camino) if camino else set()

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
                elif self.grid[r][c] == 1:
                    fila += " X"
                else:
                    fila += " ."

            print(fila)
        print()


def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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

                h = heuristica_manhattan(vecino, meta)
                f_nuevo = nuevo_g + h

                heapq.heappush(open_heap, (f_nuevo, nuevo_g, vecino))

    return []


def main():
    print("Busqueda A*")
    print("=" * 20)

    laberinto = Laberinto()
    inicio = (0, 0)
    meta = (4, 4)

    print("\nCuadricula inicial")
    print("S -> Inicio   F -> Meta   X -> Obstaculo   . -> Libre")
    laberinto.imprimir(inicio=inicio, meta=meta)

    print("=" * 20)
    print("Aplicando A*")
    print("=" * 20)

    camino = a_estrella(laberinto, inicio, meta)

    if camino:
        costo_total = len(camino) - 1

        print("Ruta encontrada:")
        print(camino)

        print(f"\nCosto total: {costo_total}")

        print("\nCuadricula final con la ruta marcada:")
        laberinto.imprimir(camino, inicio, meta)
    else:
        print("Sin solucion")


if __name__ == "__main__":
    main()
