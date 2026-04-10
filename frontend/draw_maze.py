from .parsing import parse_values, is_valid_data
from .themes import THEMES
import sys

SHAPE_42 = [
    "000100110",
    "000100010",
    "000110110",
    "000010100",
    "000010110",
]

N, S, E, W = 0x8, 0x4, 0x2, 0x1

RESET = "\033[0m"

theme_names = list(THEMES.keys())
theme_index = 0


def get_theme() -> dict[str, str]:
    import frontend as ui
    return ui.THEMES[ui.theme_names[ui.theme_index]]


def is_42(r: int, c: int, start_r: int, start_c: int) -> bool:
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


def cell_has_wall(
    grid: list[list[int]], r: int, c: int, direction: int,
    start_r: int, start_c: int
) -> bool:
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


def build_maze(
    grid: list[list[int]], entry: tuple[int, int], exit_: tuple[int, int],
    path: list[tuple[int, int]] | None = None
) -> str:
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
    PATH = t.get("path", "\033[46m")

    path_set = set(path) if path else set()

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
            elif (r, c) in path_set:
                fill = PATH
            else:
                fill = PASSAGE

            row += fill + "   " + RESET

            has_east_wall = cell_has_wall(
                grid, r, c, E, start_r, start_c
            )
            right_in_42 = is_42(r, c + 1, start_r, start_c)

            if in_42 and right_in_42:
                row += NUMBER + " " + RESET
            else:
                east_on_path = (
                    not has_east_wall
                    and (r, c) in path_set
                    and (r, c + 1) in path_set
                )
                row += (
                    PATH if east_on_path
                    else WALL if has_east_wall
                    else PASSAGE
                ) + " " + RESET

        out.append(row)

        wall_row = WALL + " " + RESET
        for c in range(cols):
            in_42 = is_42(r, c, start_r, start_c)
            below_in_42 = is_42(r + 1, c, start_r, start_c)
            has_south_wall = cell_has_wall(
                grid, r, c, S, start_r, start_c
            )

            if in_42 and below_in_42:
                wall_row += NUMBER + "   " + RESET
            else:
                south_on_path = (
                    not has_south_wall
                    and (r, c) in path_set
                    and (r + 1, c) in path_set
                )
                color = (
                    PATH if south_on_path
                    else WALL if has_south_wall
                    else PASSAGE
                )
                wall_row += color + "   " + RESET

            wall_row += WALL + " " + RESET

        out.append(wall_row)

    return "\n".join(out)


def render_maze(config_file: str) -> None:
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


def render_solution(config_file: str) -> None:
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

    entry = configs["ENTRY"]
    exit_ = configs["EXIT"]

    # Hardcoded — substituir pelo output do algoritmo
    hardcoded_path = [
        (entry[1],      entry[0]),
        (entry[1],      entry[0] + 1),
        (entry[1],      entry[0] + 2),
        (entry[1],      entry[0] + 3),
        (entry[1],      entry[0] + 4),
        (entry[1],      entry[0] + 5),
        (entry[1],      entry[0] + 6),
        (entry[1],      entry[0] + 7),
        (entry[1],      entry[0] + 8),
        (entry[1],      entry[0] + 9),
        (entry[1],      entry[0] + 10),
        (entry[1],      entry[0] + 11),
        (entry[1],      entry[0] + 12),
        (entry[1],      entry[0] + 13),
        (entry[1],      entry[0] + 14),
        (entry[1],      entry[0] + 15),
        (entry[1],      entry[0] + 16),
        (entry[1],      entry[0] + 17),
        (entry[1],      entry[0] + 18),
        (entry[1],      entry[0] + 19),
        (entry[1] + 1,  entry[0] + 19),
        (entry[1] + 2,  entry[0] + 19),
        (entry[1] + 3,  entry[0] + 19),
        (entry[1] + 4,  entry[0] + 19),
        (entry[1] + 5,  entry[0] + 19),
        (entry[1] + 6,  entry[0] + 19),
        (entry[1] + 7,  entry[0] + 19),
        (entry[1] + 8,  entry[0] + 19),
        (entry[1] + 9,  entry[0] + 19),
        (entry[1] + 10, entry[0] + 19),
        (entry[1] + 11, entry[0] + 19),
        (entry[1] + 12, entry[0] + 19),
        (entry[1] + 13, entry[0] + 19),
        (entry[1] + 14, entry[0] + 19),
        (entry[1] + 15, entry[0] + 19),
    ]

    print(build_maze(grid, entry=entry, exit_=exit_, path=hardcoded_path))
