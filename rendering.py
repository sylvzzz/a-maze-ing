import sys
import os
from parsing import parse_values, is_valid_data

# Direções (Bitmask)
N, S, E, W = 0x8, 0x4, 0x2, 0x1


def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


RESET = "\033[0m"

# Cores
WALL = bg(220, 220, 220)
PASSAGE = bg(10, 10, 10)
ENTRY = bg(180, 0, 220)
EXIT = bg(200, 30, 30)
NUMBER = bg(180, 180, 180)  # Cor cinza claro para o "42"

# 🔢 Matriz do "42" (1 = Bloco, 0 = Fundo)
SHAPE_42 = [
    "100010011110",
    "100010010001",
    "111110000110",
    "000010001000",
    "000010011111",
]


def is_42(r, c, start_r, start_c):
    rr = r - start_r
    cc = c - start_c
    if 0 <= rr < len(SHAPE_42) and 0 <= cc < len(SHAPE_42[0]):
        return SHAPE_42[rr][cc] == "1"
    return False


def parse_grid(path: str) -> list[list[int]]:
    grid = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                grid.append([int(v, 16) for v in line.split()])
    except FileNotFoundError:
        print(f"Erro: ficheiro '{path}' não encontrado.")
        sys.exit(1)
    return grid


def cell_has_wall(grid: list[list[int]], r: int, c: int, direction: int,
                  start_r: int, start_c: int) -> bool:
    """
    Devolve True se deve ser desenhada uma parede nessa direção.
    Regras:
      1. Se a célula atual pertence ao "42" → sempre parede em todas as direções.
      2. Se a célula vizinha (na direção pedida) pertence ao "42" → parede também.
      3. Caso contrário, usa o bitmask normal do grid.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Célula atual é parte do "42"
    if is_42(r, c, start_r, start_c):
        return True

    # Verificar vizinho na direção
    if direction == S:
        nr, nc = r + 1, c
    elif direction == N:
        nr, nc = r - 1, c
    elif direction == E:
        nr, nc = r, c + 1
    elif direction == W:
        nr, nc = r, c - 1
    else:
        nr, nc = r, c

    # Vizinho dentro dos limites e faz parte do "42"
    if 0 <= nr < rows and 0 <= nc < cols:
        if is_42(nr, nc, start_r, start_c):
            return True

    # Lógica normal: bit do grid
    return bool(grid[r][c] & direction)


def render(grid: list[list[int]], entry: tuple, exit_: tuple) -> str:
    rows, cols = len(grid), len(grid[0])

    entry_pos = (entry[1], entry[0])
    exit_pos = (exit_[1], exit_[0])

    # Centralizar o "42"
    start_r = rows // 2 - 2
    start_c = cols // 2 - 6

    out = []

    # Borda superior do labirinto
    out.append(WALL + " " * (cols * 4 + 1) + RESET)

    for r in range(rows):
        # Parede lateral esquerda
        row = WALL + " " + RESET

        for c in range(cols):
            in_42 = is_42(r, c, start_r, start_c)

            # Cor da célula
            if in_42:
                fill = NUMBER
            elif (r, c) == entry_pos:
                fill = ENTRY
            elif (r, c) == exit_pos:
                fill = EXIT
            else:
                fill = PASSAGE

            row += fill + "   " + RESET

            # Parede ESTE (direita)
            has_east_wall = cell_has_wall(grid, r, c, E, start_r, start_c)

            # Se ambas as células (atual e direita) são "42", conector também é "42"
            right_in_42 = is_42(r, c + 1, start_r, start_c)
            if in_42 and right_in_42:
                row += NUMBER + " " + RESET
            else:
                row += (WALL if has_east_wall else PASSAGE) + " " + RESET

        out.append(row)

        # Linha de paredes SUL (baixo)
        wall_row = WALL + " " + RESET
        for c in range(cols):
            in_42 = is_42(r, c, start_r, start_c)
            below_in_42 = is_42(r + 1, c, start_r, start_c)

            has_south_wall = cell_has_wall(grid, r, c, S, start_r, start_c)

            # Se célula atual e a de baixo são "42", conector também é "42"
            if in_42 and below_in_42:
                wall_row += NUMBER + "   " + RESET
            else:
                wall_row += (WALL if has_south_wall else PASSAGE) + "   " + RESET

            # Quina
            wall_row += WALL + " " + RESET

        out.append(wall_row)

    return "\n".join(out)


def main() -> None:
    configs = parse_values()

    if not is_valid_data(configs):
        sys.exit(1)

    output_file = configs.get("OUTPUT_FILE", "maze.txt")
    grid = parse_grid(output_file)

    expected_rows = configs["HEIGHT"]
    expected_cols = configs["WIDTH"]
    if len(grid) != expected_rows or any(len(row) != expected_cols for row in grid):
        print("Erro: Dimensões do grid inconsistentes com config.txt")
        sys.exit(1)

    print(render(grid, entry=configs["ENTRY"], exit_=configs["EXIT"]))


if __name__ == "__main__":
    while True:
        os.system("clear")
        print("\n")
        main()
        print("\n" + "=" * 20)
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print("3. Rotate colors")
        print("4. Quit")
        try:
            choice = input("Choice? (1-4): ")
            if choice == '4':
                break
        except EOFError:
            break