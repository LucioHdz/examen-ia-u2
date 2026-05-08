import heapq


cuadricula = [
    ["S", ".", ".", "X", "."],
    [".", "X", ".", "X", "."],
    [".", "X", ".", ".", "."],
    [".", ".", "X", "X", "."],
    ["X", ".", ".", ".", "F"]
]


inicio = (0, 0)
meta = (4, 4)


def heuristica_manhattan(actual, meta):
    return abs(actual[0] - meta[0]) + abs(actual[1] - meta[1])


def es_valido(fila, columna):
    if fila < 0 or fila >= len(cuadricula):
        return False

    if columna < 0 or columna >= len(cuadricula[0]):
        return False

    if cuadricula[fila][columna] == "X":
        return False

    return True


def obtener_vecinos(nodo):
    fila, columna = nodo

    movimientos = [
        (-1, 0),  
        (1, 0),  
        (0, -1),  
        (0, 1)   
    ]

    vecinos = []

    for mov_fila, mov_columna in movimientos:
        nueva_fila = fila + mov_fila
        nueva_columna = columna + mov_columna

        if es_valido(nueva_fila, nueva_columna):
            vecinos.append((nueva_fila, nueva_columna))

    return vecinos


def reconstruir_camino(came_from, actual):
    camino = [actual]

    while actual in came_from:
        actual = came_from[actual]
        camino.append(actual)

    camino.reverse()
    return camino


def algoritmo_a_estrella(inicio, meta):
    lista_abierta = []

    heapq.heappush(lista_abierta, (0, inicio))

    came_from = {}

    costo_g = {}
    costo_g[inicio] = 0

    while lista_abierta:
        _, actual = heapq.heappop(lista_abierta)

        if actual == meta:
            return reconstruir_camino(came_from, actual)

        for vecino in obtener_vecinos(actual):
            nuevo_costo = costo_g[actual] + 1

            if vecino not in costo_g or nuevo_costo < costo_g[vecino]:
                costo_g[vecino] = nuevo_costo

                costo_f = nuevo_costo + heuristica_manhattan(vecino, meta)

                heapq.heappush(lista_abierta, (costo_f, vecino))

                came_from[vecino] = actual

    return None


def imprimir_cuadricula(camino):
    copia = [fila[:] for fila in cuadricula]

    for fila, columna in camino:
        if copia[fila][columna] != "S" and copia[fila][columna] != "F":
            copia[fila][columna] = "*"

    for fila in copia:
        print(" ".join(fila))


def main():
    print("Busqueda A* en una cuadricula")
    print("=" * 35)

    camino = algoritmo_a_estrella(inicio, meta)

    if camino:
        print("\nRuta encontrada:")
        print(camino)

        costo_total = len(camino) - 1
        print("\nCosto total:", costo_total)

        print("\nCuadricula final con la ruta marcada:")
        imprimir_cuadricula(camino)

    else:
        print("No se encontro una ruta.")


if __name__ == "__main__":
    main()