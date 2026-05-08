
import math
import heapq
from collections import defaultdict
import random

class Laberinto:
    def __init__(self, filas=None, cols=None, grid_str=None):
        if grid_str:
            self.grid = self._parse_grid(grid_str)
            self.filas = len(self.grid)
            self.cols = len(self.grid[0]) if self.grid else 0
        else:
            self.filas = filas
            self.cols = cols
            self.grid = self._generar()
    
    def _parse_grid(self, grid_str):
        lines = [line.strip() for line in grid_str.strip().split('\n') if line.strip()]
        grid = []
        for line in lines:
            row = []
            for char in line.split():
                if char == 'S' or char == '.':
                    row.append(0)  # libre
                elif char == 'X':
                    row.append(1)  # obstaculo
                elif char == 'F':
                    row.append(0)  # meta
            grid.append(row)
        return grid
    
    def es_valido(self,r,c):
        return (
            0 <= r<self.filas and
            0 <= c<self.cols and
            self.grid[r][c] == 0
                )
    def vecinos(self, r,c):
        dirs = [(-1 , 0), (1 , 0), (0 , -1), (0 , 1)]
        return [(r + dr , c + dc ) for dr, dc in dirs if self.es_valido(r + dr, c + dc )]
    
    def imprimir(self, camino:list = None, inicio = None, meta = None ):
        if inicio is None:
            inicio = (0, 0)
        if meta is None:
            meta = (self.filas-1, self.cols-1)
        camino_set = set(camino) if camino else set()

        simbolos = { 0:"·", 1:"X" }

        print()
        for r in range(self.filas):
            fila = ""
            for c in range(self.cols):
                pos = (r,c)
                if pos == inicio :
                    fila += " S"
                elif pos == meta:
                    fila += " F"
                elif pos in camino_set:
                    fila += " *"
                else:
                    fila += f" {simbolos[self.grid[r][c]]}"
            print(fila)
        print()

 # Heuristica #

def heuristica_manhattan( a , b ):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(laberinto:Laberinto, inicio, meta):
    """
    A* con heurística Manhattan
    """
    def h(nodo):
        return heuristica_manhattan(nodo, meta)

    open_heap=[]
    heapq.heappush(open_heap,(h(inicio), 0, inicio))

    g_cost = defaultdict(lambda:math.inf)
    g_cost [inicio] = 0

    padre = {inicio:None}
    visitados = set()

    while open_heap:
        f , g, nodo = heapq.heappop(open_heap)
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
                padre [vecino] = nodo
                h_nuevo = nuevo_g + h(vecino)   
                heapq.heappush(open_heap, (h_nuevo, nuevo_g, vecino))
    return [] # sin solucion

def main():
    print("Examén con A*")
    print("="*30)
    

    laberinto_exa = """
S . . X .
. X . X .
. X . . .
. . X X .
X . . . F
"""
    
    laberinto = Laberinto(grid_str=laberinto_exa)
    inicio = (0,0)
    meta = (laberinto.filas-1, laberinto.cols-1)

    print(f"\nLaberinto {laberinto.filas} x {laberinto.cols} \nS -> Inicio  F -> Meta X -> Obstaculo · -> Libre")
    laberinto.imprimir(inicio=inicio, meta=meta)

    print("="*20)
    print("A* con heurística Manhattan: ")

    camino = a_estrella(laberinto, inicio, meta)
    if camino :
        print(f"Longitud del camino es: {len(camino)} nodos")
        print("\nRuta encontrada con A*:")
        laberinto.imprimir(camino, inicio, meta)
    else:
        print(" Sin Solución :()")

if __name__ == "__main__":
    main() 
