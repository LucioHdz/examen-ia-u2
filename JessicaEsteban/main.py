import heapq

class Nodo:
    def __init__(self, posicion, g=0, h=0, padre=None):
        self.posicion = posicion
        self.g = g
        self.h = h  
        self.f = g + h  
        self.padre = padre

    # Esto permite que heapq compare los nodos por su valor F
    def __lt__(self, otro):
        return self.f < otro.f

def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def resolver_a_estrella(mapa, inicio_pos, meta_pos):
    filas, cols = len(mapa), len(mapa[0])
    
    # Lista abierta (prioridad) y lista cerrada (visitados)
    lista_abierta = []
    visitados = {} # posicion: costo_g

    # Crear nodo inicial
    inicio_nodo = Nodo(inicio_pos, g=0, h=heuristica_manhattan(inicio_pos, meta_pos))
    heapq.heappush(lista_abierta, inicio_nodo)

    while lista_abierta:
        nodo_actual = heapq.heappop(lista_abierta)

        # Si ya visitamos este punto con un costo menor, saltamos
        if nodo_actual.posicion in visitados and visitados[nodo_actual.posicion] <= nodo_actual.g:
            continue
        
        visitados[nodo_actual.posicion] = nodo_actual.g

        # ¿Llegamos a la meta?
        if nodo_actual.posicion == meta_pos:
            camino = []
            costo_total = nodo_actual.g
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1], costo_total

        # Generar vecinos (Arriba, Abajo, Izquierda, Derecha)
        r, c = nodo_actual.posicion
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < filas and 0 <= nc < cols and mapa[nr][nc] != 'X':
                pos_vecino = (nr, nc)
                nuevo_g = nodo_actual.g + 1
                
                h_vecino = heuristica_manhattan(pos_vecino, meta_pos)
                vecino_nodo = Nodo(pos_vecino, nuevo_g, h_vecino, nodo_actual)
                
                heapq.heappush(lista_abierta, vecino_nodo)

    return None, None

# --- Datos del problema ---
grid = [
    ['S', '.', '.', 'X', '.'],
    ['.', 'X', '.', 'X', '.'],
    ['.', 'X', '.', '.', '.'],
    ['.', '.', 'X', 'X', '.'],
    ['X', '.', '.', '.', 'F']
]

inicio = (0, 0)
meta = (4, 4)

# Ejecución y visualización
ruta, costo = resolver_a_estrella(grid, inicio, meta)

if ruta:
    print(f"Ruta: {ruta}")
    print(f"Costo Total: {costo}")
    
    # Marcar ruta
    for r, c in ruta:
        if grid[r][c] == '.': grid[r][c] = '*'
    
    print("\nMapa Resultante:")
    for fila in grid:
        print(" ".join(fila))
