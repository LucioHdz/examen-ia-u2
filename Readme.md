# Examen Unidad 2

## Instrucciones generales

- El examen es individual.
- El proyecto deberá desarrollarse en Python.
- No se permite copiar código de otros compañeros.
- El proyecto deberá subirse a este repositorio en una carpeta con el nombre completo del alumno o número de control.
- El código debe ser funcional, ordenado y ejecutarse correctamente.

## Estructura de entrega

Cada alumno deberá crear una carpeta con la siguiente estructura:

```txt
/NombreApellido/
    main.py
    README.md
```

Ejemplo:

```txt
/JuanPerez/
    main.py
    README.md
```

## Problema a resolver

Desarrollar un programa que implemente el algoritmo A* para encontrar la ruta más corta dentro de una cuadrícula con obstáculos.

### Cuadrícula

```txt
S . . X .
. X . X .
. X . . .
. . X X .
X . . . F
```

Donde:

- `S` representa el punto inicial `(0,0)`
- `F` representa la meta `(4,4)`
- `X` representa obstáculos
- `.` representa espacios transitables

## Requisitos obligatorios

El programa deberá incluir:

- Implementación del algoritmo A*
- Uso de heurística Manhattan
- Movimientos únicamente:
  - arriba
  - abajo
  - izquierda
  - derecha
- Cada movimiento tendrá un costo de `1`

## Salida esperada

El programa deberá mostrar:

- Ruta encontrada
- Costo total
- Cuadrícula final con la ruta marcada mediante `*`

## Criterios de evaluación

| Campo | Porcentaje |
|---|---|
| Implementa correctamente el algoritmo A* | 20% |
| Utiliza heurística Manhattan | 20% |
| Encuentra y muestra la ruta final | 10% |
| Muestra la cuadrícula con la ruta marcada | 5% |
| Código ordenado y funcional | 5% |

## Entrega

Subir el proyecto completo antes de las 11:00 a.m. del 5 de mayo del 2026.
