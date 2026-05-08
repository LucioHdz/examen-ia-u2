import heapq

def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(cuadricula, inicio, meta):
    filas = len(cuadricula)
    cols = len(cuadricula[0])
    
    open_heap = []
    heapq.heappush(open_heap, (heuristica_manhattan(inicio, meta), 0, inicio))
    
    g_cost = {inicio: 0}
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
            return camino[::-1], g  
        r, c = nodo
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < filas and 0 <= nc < cols and cuadricula[nr][nc] != 'X':
                vecino = (nr, nc)
                nuevo_g = g + 1 # Costo de movimiento = 1
                
                if vecino not in g_cost or nuevo_g < g_cost[vecino]:
                    g_cost[vecino] = nuevo_g
                    padre[vecino] = nodo
                    f_nuevo = nuevo_g + heuristica_manhattan(vecino, meta)
                    heapq.heappush(open_heap, (f_nuevo, nuevo_g, vecino))
                    
    return None, None # No hay ruta

def imprimir_resultado(cuadricula, ruta, costo):
    if not ruta:
        print("No se encontró una ruta válida.")
        return

    for r, c in ruta:
        if cuadricula[r][c] == '.':
            cuadricula[r][c] = '*'

    print(f"Ruta encontrada: {ruta}")
    print(f"Costo total: {costo}")
    print("\nCuadricula Final:")
    for fila in cuadricula:
        print(" ".join(fila))


mapa = [
    ['S', '.', '.', 'X', '.'],
    ['.', 'X', '.', 'X', '.'],
    ['.', 'X', '.', '.', '.'],
    ['.', '.', 'X', 'X', '.'],
    ['X', '.', '.', '.', 'F']
]

punto_inicio = (0, 0)
punto_meta = (4, 4)

ruta_final, costo_final = a_estrella(mapa, punto_inicio, punto_meta)
imprimir_resultado(mapa, ruta_final, costo_final)
