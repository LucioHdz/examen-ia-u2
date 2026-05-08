import heapq

class Nodo:
    def __init__(self, posicion, padre=None):
        self.posicion = posicion
        self.padre = padre
        self.g = 0 # Costo desde el inicio
        self.h = 0 # Heurística (distancia Manhattan al final)
        self.f = 0 # Costo total (g + h)

    def __eq__(self, otro):
        return self.posicion == otro.posicion
    
    def __lt__(self, otro):
        return self.f < otro.f

def distancia_manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def obtener_vecinos(cuadricula, nodo):
    vecinos = []
    # Arriba, Abajo, Izquierda, Derecha
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for mov_fila, mov_col in direcciones:
        nueva_fila = nodo.posicion[0] + mov_fila
        nueva_col = nodo.posicion[1] + mov_col
        
        # Verificar límites de la cuadrícula
        if (nueva_fila < 0 or nueva_fila >= len(cuadricula) or 
            nueva_col < 0 or nueva_col >= len(cuadricula[0])):
            continue
            
        # Verificar obstáculos
        if cuadricula[nueva_fila][nueva_col] == 'X':
            continue
            
        nuevo_nodo = Nodo((nueva_fila, nueva_col), nodo)
        vecinos.append(nuevo_nodo)
        
    return vecinos

def algoritmo_a_estrella(cuadricula, inicio, meta):
    nodo_inicio = Nodo(inicio)
    nodo_meta = Nodo(meta)

    lista_abierta = []
    lista_cerrada = set()

    # Añadir el nodo inicial a la lista abierta
    heapq.heappush(lista_abierta, (nodo_inicio.f, id(nodo_inicio), nodo_inicio))

    while len(lista_abierta) > 0:
        # Obtener el nodo con el menor valor f
        nodo_actual = heapq.heappop(lista_abierta)[2]
        lista_cerrada.add(nodo_actual.posicion)

        # Si hemos llegado a la meta
        if nodo_actual == nodo_meta:
            ruta = []
            actual = nodo_actual
            while actual is not None:
                ruta.append(actual.posicion)
                actual = actual.padre
            return ruta[::-1] # Invertir ruta para que vaya de inicio a fin

        # Generar vecinos
        vecinos = obtener_vecinos(cuadricula, nodo_actual)

        for vecino in vecinos:
            # Si el vecino ya fue evaluado, ignorarlo
            if vecino.posicion in lista_cerrada:
                continue

            # El costo de cada movimiento es 1
            vecino.g = nodo_actual.g + 1
            vecino.h = distancia_manhattan(vecino.posicion, nodo_meta.posicion)
            vecino.f = vecino.g + vecino.h

            # Verificar si un nodo con la misma posición ya está en la lista abierta con menor costo
            en_abierta = False
            for item in lista_abierta:
                nodo_en_abierta = item[2]
                if vecino == nodo_en_abierta and vecino.g >= nodo_en_abierta.g:
                    en_abierta = True
                    break
            
            if not en_abierta:
                heapq.heappush(lista_abierta, (vecino.f, id(vecino), vecino))

    return None # No se encontró ruta

def imprimir_cuadricula_con_ruta(cuadricula, ruta, inicio, meta):
    # Crear una copia de la cuadrícula para no modificar la original
    cuadricula_final = [fila[:] for fila in cuadricula]
    
    # Marcar la ruta con '*' excluyendo el inicio y la meta
    for posicion in ruta:
        if posicion != inicio and posicion != meta:
            cuadricula_final[posicion[0]][posicion[1]] = '*'
            
    # Imprimir la cuadrícula
    for fila in cuadricula_final:
        print(" ".join(fila))

def main():
    # Definición de la cuadrícula original
    representacion = [
        "S . . X .",
        ". X . X .",
        ". X . . .",
        ". . X X .",
        "X . . . F"
    ]

    # Convertir a matriz 2D
    cuadricula = [fila.split() for fila in representacion]
    
    inicio = (0, 0)
    meta = (4, 4)

    # Ejecutar el algoritmo A*
    ruta = algoritmo_a_estrella(cuadricula, inicio, meta)

    if ruta:
        # Restamos 1 al costo total porque la posición inicial no cuenta como movimiento
        costo_total = len(ruta) - 1 
        
        print(f"Ruta encontrada: {ruta}")
        print(f"Costo total: {costo_total}")
        print("\nCuadrícula final:")
        imprimir_cuadricula_con_ruta(cuadricula, ruta, inicio, meta)
    else:
        print("No se encontró ninguna ruta hacia la meta.")

if __name__ == "__main__":
    main()



