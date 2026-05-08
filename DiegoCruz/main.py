# Mostrar unicamente movimientos de arriba, abajo, izquierda y derecha
# Cada movimiento con un coste de 1

# Debe inclur el algoritmo A*, haciendo uso de una heurística basada en distancia Manhattan

# Debe mostrar la ruta encontrada, el costo total, y la cuadrícula final con la ruta marcada mediante *

import heapq


class Laberinto:
    def __init__(self):
        self.grid = [
            [0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0],
        ]

        self.filas = len(self.grid)
        self.cols = len(self.grid[0])

    def es_valido(self, r, c):
        dentro = 0 <= r < self.filas and 0 <= c < self.cols

        if not dentro:
            return False

        return self.grid[r][c] == 0

    def vecinos(self, r, c):
        dirs = [
            (-1, 0),  # arriba
            (1, 0),   # abajo
            (0, -1),  # izquierda
            (0, 1),   # derecha
        ]

        resultado = []

        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc

            if self.es_valido(nr, nc):
                resultado.append((nr, nc))

        return resultado

    def imprimir(self, camino=None, inicio=(0, 0), meta=None):
        if meta is None:
            meta = (self.filas - 1, self.cols - 1)

        camino = camino if camino else []
        camino_set = set(camino)

        print()
        for r in range(self.filas):
            fila = []

            for c in range(self.cols):
                pos = (r, c)

                if pos == inicio:
                    fila.append("S")
                elif pos == meta:
                    fila.append("F")
                elif pos in camino_set:
                    fila.append("*")
                elif self.grid[r][c] == 1:
                    fila.append("X")
                else:
                    fila.append(".")

            print(" ".join(fila))
        print()


def heuristica_manhattan(a, b):
    distancia_filas = abs(a[0] - b[0])
    distancia_columnas = abs(a[1] - b[1])

    return distancia_filas + distancia_columnas


def a_estrella(laberinto: Laberinto, inicio, meta):
    open_heap = []
    heapq.heappush(open_heap, (0, inicio))

    g_cost = {
        inicio: 0
    }

    padre = {
        inicio: None
    }

    visitados = set()

    while len(open_heap) > 0:
        _, nodo = heapq.heappop(open_heap)

        if nodo in visitados:
            continue

        visitados.add(nodo)

        if nodo == meta:
            camino = []

            actual = nodo
            while actual is not None:
                camino.insert(0, actual)
                actual = padre[actual]

            return camino

        for vecino in laberinto.vecinos(nodo[0], nodo[1]):
            nuevo_g = g_cost[nodo] + 1

            if vecino not in g_cost or nuevo_g < g_cost[vecino]:
                g_cost[vecino] = nuevo_g
                padre[vecino] = nodo

                h = heuristica_manhattan(vecino, meta)
                prioridad = nuevo_g + h

                heapq.heappush(open_heap, (prioridad, vecino))

    return []


def main():
    laberinto = Laberinto()

    inicio = (0, 0)
    meta = (4, 4)

    print("Cuadricula inicial:")
    print("S = inicio | F = meta | X = obstaculo | . = libre")
    laberinto.imprimir(inicio=inicio, meta=meta)

    camino = a_estrella(laberinto, inicio, meta)

    if len(camino) > 0:
        print("Ruta encontrada:")
        print(camino)

        costo_total = len(camino) - 1
        print("\nCosto total:", costo_total)

        print("\nCuadricula final:")
        laberinto.imprimir(camino, inicio, meta)
    else:
        print("No se encontro una ruta.")


if __name__ == "__main__":
    main()
