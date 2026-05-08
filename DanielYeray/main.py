import math
import heapq
from collections import defaultdict

class Laberinto:
    def __init__(self):
        self.filas = 5
        self.cols = 5
        
    def es_obstaculo(self, r, c):
        # Obstaculos en sus posiciones
        obstaculos = {(0, 3), (1, 1), (1, 3), 
                    (2, 1), (3, 2), (3, 3), 
                    (4, 0)}
        return (r, c) in obstaculos
    
    def es_valido(self, r, c):
        return (0 <= r < self.filas and 
                0 <= c < self.cols and 
                not self.es_obstaculo(r, c))
    
    def vecinos(self, r, c):
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if self.es_valido(r + dr, c + dc)]
    
    def imprimir(self, camino:list = None, inicio=(0,0), meta=None):
        meta = meta or (self.filas-1, self.cols-1)
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
                elif self.es_obstaculo(r, c):
                    fila += " X"
                else:
                    fila += " ."
            print(fila)
        print()
        
def heuristica_manhattan(a, b):
    # Distancia Manhattan pura
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(laberinto: Laberinto, inicio, meta):
    """
    Algoritmo A* puro con heurística de Manhattan.
    """
    def h(nodo):
        return heuristica_manhattan(nodo, meta)

    open_heap = []
    heapq.heappush(open_heap, (h(inicio), 0, inicio))

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
            # Reconstruir nuestro camino
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
                h_nuevo = nuevo_g + h(vecino)
                heapq.heappush(open_heap, (h_nuevo, nuevo_g, vecino))
                
    return []  # No hay solución
    
def main():
    laberinto = Laberinto()
    inicio = (0, 0)
    meta = (4, 4)
    
    camino = a_estrella(laberinto, inicio, meta)
    
    if camino:
        print("Ruta encontrada")
        print(f"Costo total: {len(camino) - 1}")
        print("Cuadrícula final con la ruta marcada mediante *:")
        laberinto.imprimir(camino, inicio, meta)
    else: 
        print("No hay solucion :C")
    
if __name__ == "__main__":
    main()