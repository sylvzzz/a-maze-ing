# directions constants
N = "N"
E = "E"
S = "S"
W = "W"
# all directions
DIRECTIONS = [N, E, S, W]
# movement vectors
MOVES = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}
# opposite directions
OPPOSITE = {
    N: S,
    S: N,
    E: W,
    W: E
}
# bit encoding values
BIT_VALUES = {
    N: 1,
    E: 2,
    S: 4,
    W: 8
}
