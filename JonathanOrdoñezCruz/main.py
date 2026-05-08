import heapq
from collections import defaultdict

def heuristica_manhattan(a, b):
    """Distancia Manhattan entre dos puntos"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(laberinto, inicio, meta):
    filas = len(laberinto)
    cols = len(laberinto[0])
    
    def es_valido(r, c):
        return 0 <= r < filas and 0 <= c < cols and laberinto[r][c] == 0
    
    def vecinos(r, c):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if es_valido(r + dr, c + dc)]
    
    
    open_heap = []
    heapq.heappush(open_heap, (heuristica_manhattan(inicio, meta), 0, inicio))
    
    
    g_cost = defaultdict(lambda: float('inf'))
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
        
        
        for vecino in vecinos(*nodo):
            nuevo_g = g + 1
            if nuevo_g < g_cost[vecino]:
                g_cost[vecino] = nuevo_g
                padre[vecino] = nodo
                h = heuristica_manhattan(vecino, meta)
                f_nuevo = nuevo_g + h
                heapq.heappush(open_heap, (f_nuevo, nuevo_g, vecino))
    
    return [] 

def imprimir_laberinto_con_camino(laberinto, camino, inicio, meta):
    simbolos = {0: '.', 1: 'X'}
    camino_set = set(camino)
    
    print("\n")
    print("LABERINTO CON RUTA ENCONTRADA")
    
    for r in range(len(laberinto)):
        fila = ""
        for c in range(len(laberinto[0])):
            pos = (r, c)
            if pos == inicio:
                fila += "S "
            elif pos == meta:
                fila += "F "
            elif pos in camino_set and laberinto[r][c] == 0:
                fila += "* "
            else:
                fila += f"{simbolos[laberinto[r][c]]} "
        print(fila)
    print()

def main():
   
    laberinto = [
        [0, 0, 0, 1, 0],  
        [0, 1, 0, 1, 0],  
        [0, 1, 0, 0, 0],  
        [0, 0, 1, 1, 0],
        [1, 0, 0, 0, 0]
    ]
    
    inicio = (0, 0)
    meta = (4, 4)
    
    print("\n")
    print("IMPLEMENTACIÓN DEL ALGORITMO A*")
    print("\n")
    print("\nLaberinto original:")
    
    for r in range(len(laberinto)):
        fila = ""
        for c in range(len(laberinto[0])):
            if (r, c) == inicio:
                fila += "S "
            elif (r, c) == meta:
                fila += "F "
            elif laberinto[r][c] == 1:
                fila += "X "
            else:
                fila += ". "
        print(fila)
    
    camino = a_estrella(laberinto, inicio, meta)
    
    if camino:
        costo_total = len(camino) - 1 
        
        print(f"\nRUTA ENCONTRADA")
        print(f"Costo total: {costo_total} pasos")
        imprimir_laberinto_con_camino(laberinto, camino, inicio, meta)
        
    else:
        print("\n✗ NO SE ENCONTRÓ UNA RUTA VÁLIDA ✗")
        print("No hay camino posible desde S hasta F")

if __name__ == "__main__":
    main()
