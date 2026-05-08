import math
import random
import heapq
from collections import defaultdict

# =========================
# LABERINTO INICIAN FIJO
# =========================
class Laberinto:

    def __init__(self, filas, cols):

        self.filas = filas
        self.cols = cols

        # Cuadrícula fija del examen
        self.grid = [
            ['S', '.', '.', 'X', '.'],
            ['.', 'X', '.', 'X', '.'],
            ['.', 'X', '.', '.', '.'],
            ['.', '.', 'X', 'X', '.'],
            ['X', '.', '.', '.', 'F']
        ]

    def es_valido(self, r, c):

        return (
            0 <= r < self.filas and
            0 <= c < self.cols and
            self.grid[r][c] != 'X'
        )

    def vecinos(self, r, c):

        dirs = [
            (-1, 0),  # arriba 
            (1, 0),   # abajo 
            (0, -1),  # izquierda
            (0, 1)    # derecha
        ]

        return [
            (r + dr, c + dc)
            for dr, dc in dirs
            if self.es_valido(r + dr, c + dc)
        ]

    def imprimir(self, camino=None, inicio=(0, 0), meta=None):

        if meta is None:
            meta = (self.filas - 1, self.cols - 1)

        camino_set = set(camino) if camino else set()

        print()

        for r in range(self.filas):

            fila = ""

            for c in range(self.cols):

                pos = (r, c)

                if pos == inicio:
                    fila += "S "

                elif pos == meta:
                    fila += "F "

                elif pos in camino_set:
                    fila += "* "

                else:
                    fila += self.grid[r][c] + " "

            print(fila)

        print()


# =========================
# HEURÍSTICA MANHATHAN 
# =========================
def heuristica_manhattan(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# =========================
# ALGORITMO IMPLEMENTADO A*
# =========================
def a_estrella(
        laberinto: Laberinto,
        inicio,
        meta
):

    open_heap = []

    heapq.heappush(
        open_heap,
        (
            heuristica_manhattan(inicio, meta),
            0,
            inicio
        )
    )

    g_cost = defaultdict(lambda: math.inf)

    g_cost[inicio] = 0

    padre = {
        inicio: None
    }

    visitados = set()

    while open_heap:

        f, g, nodo = heapq.heappop(open_heap)

        if nodo in visitados:
            continue

        visitados.add(nodo)

        # Meta encontrada
        if nodo == meta:

            camino = []

            while nodo is not None:

                camino.append(nodo)

                nodo = padre[nodo]

            return camino[::-1], g

        # Explorar vecinos
        for vecino in laberinto.vecinos(*nodo):

            nuevo_g = g + 1

            if nuevo_g < g_cost[vecino]:

                g_cost[vecino] = nuevo_g

                padre[vecino] = nodo

                h = heuristica_manhattan(vecino, meta)

                f_nuevo = nuevo_g + h

                heapq.heappush(
                    open_heap,
                    (
                        f_nuevo,
                        nuevo_g,
                        vecino
                    )
                )

    return [], 0


# =========================
# RESULTADO VISUAL (MAIN)
# =========================
def main():

    print("Busqueda por algorito A*")
    print("=" * 30)

    FILAS, COLS = 5, 5

    laberinto = Laberinto(FILAS, COLS)

    inicio = (0, 0)

    meta = (4, 4)

    print("\nCuadrícula original:\n")

    laberinto.imprimir(
        inicio=inicio,
        meta=meta
    )

    print("=" * 20)
    print("A*")
    print("=" * 20)

    camino, costo = a_estrella(
        laberinto,
        inicio,
        meta
    )

    if camino:

        print(f"\nRuta encontrada:")
        print(camino)

        print(f"\nCosto total: {costo}")

        print("\nCuadrícula final con la ruta:\n")

        laberinto.imprimir(
            camino,
            inicio,
            meta
        )

    else:

        print("Sin solución")


# =========================
# EJECUTAR
# =========================
if __name__ == "__main__":
    main()
