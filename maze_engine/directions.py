""" PSEUDOCODIGO: maze_engine/directions.py

OBJETIVO
- Centralizar direcoes, deslocamentos e relacoes opostas.

DIRECOES CARDINAIS
- N, E, S, W

BITS DE PAREDE (consistencia com renderer)
- N = 8
- E = 2
- S = 4
- W = 1

ESTRUTURAS
- CARDINAL_DIRECTIONS = [N, E, S, W]
- DELTA_BY_DIRECTION:
  N -> (0, -1)
  E -> (1, 0)
  S -> (0, 1)
  W -> (-1, 0)
- OPPOSITE_DIRECTION:
  N <-> S
  E <-> W
- ALL_WALLS = N + E + S + W
 """

N = "N"
E = "E"
S = "S"
W = "W"

directions = [N, E, S, W]

moves = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}

opposite = {
    N: S,
    S: N,
    E: W,
    W: E
}

BIT_VALUES = {
    N: 1,
    E: 2,
    S: 4,
    W: 8
}
