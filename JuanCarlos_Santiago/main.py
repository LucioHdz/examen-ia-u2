import heapq
import random

def is_square(matriz):
    if not matriz:
        return False
    filas = len(matriz)
    for fila in matriz:
        if len(fila) != filas:
            return False
    return True

def distancia_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

class Perceptron:
    def __init__(self, n_features: int, lr: float = 0.1):
        self.lr = lr
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(n_features)]
        self.bias = random.uniform(-0.5, 0.5)
        self.history = []

    def _activacion(self, z: float) -> int:
        return 1 if z >= 0 else 0

    def predict(self, x: list) -> int:
        z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
        return self._activacion(z)

    def score(self, x: list) -> float:
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias

    def train(self, X: list, y: list, epochs: int = 50):
        for epoch in range(epochs):
            errores = 0
            for xi, yi in zip(X, y):
                pred = self.predict(xi)
                error = yi - pred
                if error != 0:
                    errores += 1
                    self.weights = [w + self.lr * error * x for w, x in zip(self.weights, xi)]
                    self.bias += self.lr * error
            self.history.append(errores)
            if errores == 0:
                break

    def accuracy(self, X: list, y: list) -> float:
        correcto = sum(1 for xi, yi in zip(X, y) if self.predict(xi) == yi)
        return correcto / len(y) if y else 0.0

class Nodo:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash((self.x, self.y))

class Laberinto:
    def __init__(self):
        self.grid = [
            [0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0]
        ]
        self.filas = len(self.grid)
        self.cols = len(self.grid[0])

        if not is_square(self.grid):
            raise ValueError("La cuadricula debe ser una matriz cuadrada")

    def es_valido(self, r: int, c: int) -> bool:
        return (0 <= r < self.filas and 0 <= c < self.cols and self.grid[r][c] == 0)

    def vecinos(self, r: int, c: int) -> list:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [(r + dr, c + dc) for dr, dc in dirs if self.es_valido(r + dr, c + dc)]

    def densidad_local(self, r: int, c: int, radio: int = 1) -> float:
        total = obstaculos = 0
        for dr in range(-radio, radio + 1):
            for dc in range(-radio, radio + 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.filas and 0 <= nc < self.cols:
                    total += 1
                    obstaculos += self.grid[nr][nc]
        return obstaculos / total if total else 0.0

    def imprimir(self, camino: list = None, inicio=(0, 0), meta=(4, 4)):
        camino_set = set(camino) if camino else set()
        print("\n  0 1 2 3 4")
        for r in range(self.filas):
            fila = f"{r} "
            for c in range(self.cols):
                pos = (r, c)
                if pos == inicio:
                    fila += "X "
                elif pos == meta:
                    fila += "F "
                elif pos in camino_set:
                    fila += "* "
                elif self.grid[r][c] == 1:
                    fila += "# "
                else:
                    fila += ". "
            print(fila)
        print()

def extraer_features(r: int, c: int, meta: tuple, laberinto: Laberinto) -> list:
    fr = r / (laberinto.filas - 1) if laberinto.filas > 1 else 0
    fc = c / (laberinto.cols - 1) if laberinto.cols > 1 else 0
    dist = distancia_manhattan(r, c, meta[0], meta[1])
    dist_norm = dist / (laberinto.filas + laberinto.cols)
    dens = laberinto.densidad_local(r, c)
    return [fr, fc, dist_norm, dens]

def a_estrella(laberinto: Laberinto, inicio: tuple, meta: tuple, perceptron: Perceptron = None, peso_aprendido: float = 0.4):
    def calcular_h(nodo_x, nodo_y):
        h_base = distancia_manhattan(nodo_x, nodo_y, meta[0], meta[1])
        if perceptron is None:
            return h_base
        feats = extraer_features(nodo_x, nodo_y, meta, laberinto)
        penalizacion = -perceptron.score(feats)
        return max(h_base + peso_aprendido * penalizacion, 0)

    open_heap = []
    nodo_inicio = Nodo(inicio[0], inicio[1])
    nodo_inicio.g = 0
    nodo_inicio.h = calcular_h(inicio[0], inicio[1])
    nodo_inicio.f = nodo_inicio.g + nodo_inicio.h
    heapq.heappush(open_heap, nodo_inicio)

    mejores_g = {nodo_inicio: 0}
    visitados = set()
    padre = {nodo_inicio: None}
    nodos_explorados = []

    while open_heap:
        nodo_actual = heapq.heappop(open_heap)

        if nodo_actual in visitados:
            continue

        visitados.add(nodo_actual)
        nodos_explorados.append((nodo_actual.x, nodo_actual.y))

        if (nodo_actual.x, nodo_actual.y) == meta:
            camino = []
            while nodo_actual is not None:
                camino.append((nodo_actual.x, nodo_actual.y))
                nodo_actual = padre[nodo_actual]
            camino_reverso = camino[::-1]
            return camino_reverso, nodos_explorados

        for nx, ny in laberinto.vecinos(nodo_actual.x, nodo_actual.y):
            vecino = Nodo(nx, ny)
            g_tentativo = mejores_g.get(nodo_actual, float('inf')) + 1

            if vecino in visitados:
                continue

            if vecino not in mejores_g or g_tentativo < mejores_g[vecino]:
                mejores_g[vecino] = g_tentativo
                padre[vecino] = nodo_actual
                vecino.g = g_tentativo
                vecino.h = calcular_h(vecino.x, vecino.y)
                vecino.f = vecino.g + vecino.h
                heapq.heappush(open_heap, vecino)

    return [], nodos_explorados

def generar_datos_entrenamiento(laberinto: Laberinto, n_rutas: int = 20):
    X, y = [], []
    meta = (laberinto.filas - 1, laberinto.cols - 1)

    for _ in range(n_rutas):
        intentos = 0
        while intentos < 50:
            r0 = random.randint(0, laberinto.filas - 1)
            c0 = random.randint(0, laberinto.cols - 1)
            if laberinto.grid[r0][c0] == 0:
                break
            intentos += 1
        else:
            continue

        inicio = (r0, c0)
        camino, _ = a_estrella(laberinto, inicio, meta, perceptron=None)
        if not camino:
            continue

        camino_set = set(camino)
        for nodo in camino:
            X.append(extraer_features(nodo[0], nodo[1], meta, laberinto))
            y.append(1)

        libres = [(r, c) for r in range(laberinto.filas) for c in range(laberinto.cols)
                  if laberinto.grid[r][c] == 0 and (r, c) not in camino_set]
        if libres:
            muestra_neg = random.sample(libres, min(len(camino) // 2 + 1, len(libres)))
            for nodo in muestra_neg:
                X.append(extraer_features(nodo[0], nodo[1], meta, laberinto))
                y.append(0)

    return X, y

def main():
    print("=" * 50)
    print("ALGORITMO A* + PERCEPTRON")
    print("CUADRÍCULA 5x5 (# = obstaculo)")
    print("=" * 50)

    laberinto = Laberinto()
    inicio = (0, 0)
    meta = (4, 4)

    if is_square(laberinto.grid):
        print("\nLa cuadricula es cuadrada")

    print("\nCUADRÍCULA ORIGINAL:")
    print("X = inicio, F = meta, # = obstaculo, . = camino")
    laberinto.imprimir(inicio=inicio, meta=meta)

    print("-" * 50)
    print("EJECUTANDO A* CON MANHATTAN PURO")
    print("-" * 50)

    camino_puro, explorados_puro = a_estrella(laberinto, inicio, meta, perceptron=None)

    if camino_puro:
        num_pasos = len(camino_puro) - 1
        print(f"\nRuta encontrada.")
        print(f"Numero de movimientos (pasos): {num_pasos}")
        print(f"Camino completo (incluyendo inicio): {camino_puro}")
        print(f"Inicio: {camino_puro[0]} -> Meta: {camino_puro[-1]}")
        print("\nRECORRIDO (* = camino tomado):")
        laberinto.imprimir(camino_puro, inicio, meta)
    else:
        print("No se encontro solucion")

    print("-" * 50)
    print("ENTRENANDO PERCEPTRON")
    print("-" * 50)

    X_train, y_train = generar_datos_entrenamiento(laberinto, n_rutas=30)
    print(f"Muestras generadas: {len(X_train)}")
    print(f"Prometedores: {sum(y_train)}")
    print(f"No prometedores: {len(y_train)-sum(y_train)}")

    perceptron = Perceptron(n_features=4, lr=0.1)
    perceptron.train(X_train, y_train, epochs=100)
    acc = perceptron.accuracy(X_train, y_train)
    print(f"Precision en entrenamiento: {acc * 100:.1f}%")

    print("-" * 50)
    print("EJECUTANDO A* CON HEURISTICA HIBRIDA")
    print("-" * 50)

    camino_ia, explorados_ia = a_estrella(laberinto, inicio, meta, perceptron=perceptron, peso_aprendido=0.5)

    if camino_ia:
        num_pasos_ia = len(camino_ia) - 1
        print(f"\nRuta encontrada.")
        print(f"Numero de movimientos (pasos): {num_pasos_ia}")
        print(f"Camino completo (incluyendo inicio): {camino_ia}")
        print(f"Inicio: {camino_ia[0]} -> Meta: {camino_ia[-1]}")
        print("\nRECORRIDO (* = camino tomado):")
        laberinto.imprimir(camino_ia, inicio, meta)
    else:
        print("No se encontro solucion")

    print("=" * 50)
    print("COMPARATIVA")
    print("=" * 50)

    if camino_puro:
        num_pasos_puro = len(camino_puro) - 1
        print(f"A* Manhattan puro:")
        print(f"  - Movimientos: {num_pasos_puro}")
        print(f"  - Camino: {camino_puro}")

    if camino_ia:
        num_pasos_ia = len(camino_ia) - 1
        print(f"A* + Perceptron:")
        print(f"  - Movimientos: {num_pasos_ia}")
        print(f"  - Camino: {camino_ia}")

    if camino_puro and camino_ia:
        num_pasos_puro = len(camino_puro) - 1
        num_pasos_ia = len(camino_ia) - 1
        if num_pasos_ia < num_pasos_puro:
            print(f"\nMejora de {num_pasos_puro - num_pasos_ia} movimientos")
        elif num_pasos_ia > num_pasos_puro:
            print(f"\nEmpeoro por {num_pasos_ia - num_pasos_puro} movimientos")
        else:
            print("\nAmbos encontraron la misma ruta")

if __name__ == "__main__":
    main()
