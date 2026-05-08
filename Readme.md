import heapq

class BuscadorRuta:
    def __init__(self):
        # S (0,0), F (4,4), X (Obstáculo), . (Camino)
        # 0 = transitable, 1 = obstáculo
        self.grid = [
            [0, 0, 0, 1, 0],  # S . . X .
            [0, 1, 0, 1, 0],  # . X . X .
            [0, 1, 0, 0, 0],  # . X . . .
            [0, 0, 1, 1, 0],  # . . X X .
            [1, 0, 0, 0, 0]   # X . . . F
        ]
        self.filas = len(self.grid)
        self.cols = len(self.grid[0])
        self.inicio = (0, 0)
        self.meta = (4, 4)
# distancia mathatan
    def heuristica_manhattan(self, a, b):
        """Calcula la distancia Manhattan entre dos puntos."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def obtener_vecinos(self, r, c):
        """Genera movimientos: arriba, abajo, izquierda, derecha."""
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        vecinos = []
        for dr, dc in direcciones:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.filas and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                vecinos.append((nr, nc))
        return vecinos
# Algoritmo A*
    def resolver_a_estrella(self):
        # priority_queue guarda (f_cost, g_cost, nodo_actual)
        pq = []
        heapq.heappush(pq, (self.heuristica_manhattan(self.inicio, self.meta), 0, self.inicio))
        
        vinculos = {self.inicio: None}
        costos_g = {self.inicio: 0}

        while pq:
            _, g_actual, nodo = heapq.heappop(pq)

            if nodo == self.meta:
                return self.reconstruir_camino(vinculos), g_actual

            for vecino in self.obtener_vecinos(*nodo):
                # Cada movimiento tiene un costo de 1
                nuevo_g = g_actual + 1
                
                if vecino not in costos_g or nuevo_g < costos_g[vecino]:
                    costos_g[vecino] = nuevo_g
                    f_cost = nuevo_g + self.heuristica_manhattan(vecino, self.meta)
                    vinculos[vecino] = nodo
                    heapq.heappush(pq, (f_cost, nuevo_g, vecino))
        
        return None, None

    def reconstruir_camino(self, vinculos):
        camino = []
        actual = self.meta
        while actual is not None:
            camino.append(actual)
            actual = vinculos[actual]
        return camino[::-1]

    def mostrar_resultados(self, camino, costo):
        if not camino:
            print("No se encontró una ruta.")
            return

        print(f"Ruta encontrada: {camino}")
        print(f"Costo total: {costo}")
        print("\nCuadrícula final:")
        
        camino_set = set(camino)
        for r in range(self.filas):
            fila_visual = ""
            for c in range(self.cols):
                pos = (r, c)
                if pos == self.inicio:
                    fila_visual += "S "
                elif pos == self.meta:
                    fila_visual += "F "
                elif pos in camino_set:
                    fila_visual += "* "
                elif self.grid[r][c] == 1:
                    fila_visual += "X "
                else:
                    fila_visual += ". "
            print(fila_visual)

# Ejecución del programa
if __name__ == "__main__":
    buscador = BuscadorRuta()
    ruta, costo_total = buscador.resolver_a_estrella()
    buscador.mostrar_resultados(ruta, costo_total)