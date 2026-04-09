import sys
import os
from parsing import parse_values, is_valid_data


# Direções (Bitmask)
N, S, E, W = 0x8, 0x4, 0x2, 0x1


def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


RESET = "\033[0m"

# Temas de cores
THEMES = {
    "Default": {
        "wall":    bg(220, 220, 220),
        "passage": bg(10, 10, 10),
        "entry":   bg(180, 0, 220),
        "exit":    bg(200, 30, 30),
        "number":  bg(180, 180, 180),
    },
    "Ocean": {
        "wall":    bg(0, 80, 120),
        "passage": bg(0, 20, 40),
        "entry":   bg(0, 200, 180),
        "exit":    bg(255, 100, 0),
        "number":  bg(0, 120, 160),
    },
    "Earthy": {
        "wall":    bg(47, 147, 1),
        "passage": bg(94, 67, 39),
        "entry":   bg(180, 220, 50),
        "exit":    bg(200, 80, 30),
        "number":  bg(0, 224, 228),
    },
    "Lava": {
        "wall":    bg(205, 49, 5),
        "passage": bg(40, 5, 5),
        "entry":   bg(255, 200, 0),
        "exit":    bg(0, 0, 0),
        "number":  bg(255, 173, 5),
    },
    "BENFICA SLB GLORIOSO": {
        "wall":    bg(210, 0, 0),
        "passage": bg(20, 5, 0),
        "entry":   bg(250, 220, 0),
        "exit":    bg(255, 255, 255),
        "number":  bg(255, 255, 255),
    },
    "PORTUGAL SELACAO DAS QUINAS CAMPEOES DO MUNDIAL 2026": {
        "wall":    bg(215, 5, 5),
        "passage": bg(40, 152, 20),
        "entry":   bg(250, 220, 0),
        "exit":    bg(255, 255, 255),
        "number":  bg(250, 246, 62),
    },
    "ZAPORTING": {
        "wall":    bg(3, 251, 62),
        "passage": bg(255, 255, 255),
        "entry":   bg(250, 220, 0),
        "exit":    bg(255, 255, 255),
        "number":  bg(0, 0, 0),
    },
}

theme_names = list(THEMES.keys())
theme_index = 0

SHAPE_42 = [
    "000100110",
    "000100010",
    "000110110",
    "000010100",
    "000010110",
]


def get_theme():
    return THEMES[theme_names[theme_index]]


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
    rows = len(grid)
    cols = len(grid[0])

    if is_42(r, c, start_r, start_c):
        return True

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

    if 0 <= nr < rows and 0 <= nc < cols:
        if is_42(nr, nc, start_r, start_c):
            return True

    return bool(grid[r][c] & direction)


def build_maze(grid: list[list[int]], entry: tuple, exit_: tuple) -> str:
    rows, cols = len(grid), len(grid[0])

    entry_pos = (entry[1], entry[0])
    exit_pos = (exit_[1], exit_[0])

    start_r = rows // 2 - 2
    start_c = cols // 2 - 6

    t = get_theme()
    WALL = t["wall"]
    PASSAGE = t["passage"]
    ENTRY = t["entry"]
    EXIT = t["exit"]
    NUMBER = t["number"]

    out = []

    out.append(WALL + " " * (cols * 4 + 1) + RESET)

    for r in range(rows):
        row = WALL + " " + RESET

        for c in range(cols):
            in_42 = is_42(r, c, start_r, start_c)

            if in_42:
                fill = NUMBER
            elif (r, c) == entry_pos:
                fill = ENTRY
            elif (r, c) == exit_pos:
                fill = EXIT
            else:
                fill = PASSAGE

            row += fill + "   " + RESET

            has_east_wall = cell_has_wall(grid, r, c, E, start_r, start_c)

            right_in_42 = is_42(r, c + 1, start_r, start_c)
            if in_42 and right_in_42:
                row += NUMBER + " " + RESET
            else:
                row += (WALL if has_east_wall else PASSAGE) + " " + RESET

        out.append(row)

        wall_row = WALL + " " + RESET
        for c in range(cols):
            in_42 = is_42(r, c, start_r, start_c)
            below_in_42 = is_42(r + 1, c, start_r, start_c)

            has_south_wall = cell_has_wall(grid, r, c, S, start_r, start_c)

            if in_42 and below_in_42:
                wall_row += NUMBER + "   " + RESET
            else:
                color = WALL if has_south_wall else PASSAGE
                wall_row += color + "   " + RESET

            wall_row += WALL + " " + RESET

        out.append(wall_row)

    return "\n".join(out)


def render_maze(config_file) -> None:
    configs = parse_values(config_file)

    if not is_valid_data(configs, config_file):
        sys.exit(1)

    output_file = configs.get("OUTPUT_FILE", "maze.txt")
    grid = parse_grid(output_file)

    expected_rows = configs["HEIGHT"]
    expected_cols = configs["WIDTH"]
    wrong_cols = any(len(row) != expected_cols for row in grid)
    if len(grid) != expected_rows or wrong_cols:
        print(f"Error: Grid dimensions dont match {config_file}")
        sys.exit(1)

    print(build_maze(grid, entry=configs["ENTRY"], exit_=configs["EXIT"]))


def show_menu(config_file: str) -> None:
    current_theme_name = theme_names[theme_index]
    render_maze(config_file)
    print("\n" + "=" * 20)
    print(f"Theme: {current_theme_name}")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path")
    print("3. Rotate colors")
    print("4. Quit")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        config_file = args[1]
        os.system("clear")
        show_menu(config_file)
        while True:
            try:
                choice = int(input("Choice? (1-4): "))
                if choice == 1:
                    print("Option (1. Re-generate a new maze) selected")
                elif choice == 2:
                    print("Option (2. Show/Hide path) selected")
                elif choice == 3:
                    os.system("clear")
                    theme_index = (theme_index + 1) % len(theme_names)
                    show_menu(config_file)
                elif choice == 4:
                    break
                else:
                    print("Option (2. Show/Hide path) selected")
                    break
            except ValueError:
                print("Please enter a number between 1-4...")
            except EOFError:
                break
    elif len(args) > 2:
        print("Too many arguments. Usage: python3 a_maze_ing.py config.txt")
    elif len(args) < 2:
        print("Too few arguments. Usage: python3 a_maze_ing.py config.txt")
