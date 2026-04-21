from frontend.parsing import parse_values, is_valid_data
from frontend.themes import THEMES
from frontend.directions import get_path
import sys


N, S, E, W = 0x1, 0x4, 0x2, 0x8

RESET = "\033[0m"

theme_names = list(THEMES.keys())
theme_index = 0


def get_theme() -> dict[str, str]:
    import frontend as ui
    return ui.THEMES[ui.theme_names[ui.theme_index]]


def parse_maze_file(maze_file: str) -> tuple[list[list[int]],
                                             tuple[int, int],
                                             tuple[int, int], list[str],
                                             set[tuple[int, int]]]:
    grid: list[list[int]] = []
    directions: list[str] = []
    entry: tuple[int, int] = (0, 0)
    exit_: tuple[int, int] = (0, 0)
    with open(maze_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                break
            grid.append([int(v, 16) for v in line.strip()])

        r, c = map(int, f.readline().strip().split(","))
        entry = (r, c)
        r, c = map(int, f.readline().strip().split(","))
        exit_ = (r, c)
        directions = list(f.readline().strip())

        stamp42: set[tuple[int, int]] = set()
        line = f.readline().strip()
        if line:
            for pair in line.split(";"):
                row, col = map(int, pair.split(","))
                stamp42.add((row, col))

    return grid, entry, exit_, directions, stamp42


def cell_has_wall(
    grid: list[list[int]], r: int, c: int, direction: int,
    stamp42: set[tuple[int, int]]
) -> bool:
    rows = len(grid)
    cols = len(grid[0])

    if (r, c) in stamp42:
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
        if (nr, nc) in stamp42:
            return True

    return bool(grid[r][c] & direction)


def build_maze(
    grid: list[list[int]], entry: tuple[int, int], exit_: tuple[int, int],
    stamp42: set[tuple[int, int]],
    path: list[tuple[int, int]] | None = None
) -> str:
    rows, cols = len(grid), len(grid[0])

    entry_pos = (entry[1], entry[0])
    exit_pos = (exit_[1], exit_[0])

    t = get_theme()
    WALL = t["wall"]
    PASSAGE = t["passage"]
    ENTRY = t["entry"]
    EXIT = t["exit"]
    NUMBER = t.get("number", WALL)
    PATH = t.get("path", "\033[46m")

    path_set = set(path) if path else set()

    out = []
    out.append(WALL + " " * (cols * 4 + 1) + RESET)

    for r in range(rows):
        row = WALL + " " + RESET

        for c in range(cols):
            in_42 = (r, c) in stamp42

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

            has_east_wall = cell_has_wall(grid, r, c, E, stamp42)
            right_in_42 = (r, c + 1) in stamp42

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
            in_42 = (r, c) in stamp42
            below_in_42 = (r + 1, c) in stamp42
            has_south_wall = cell_has_wall(grid, r, c, S, stamp42)

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


def render_maze(config_file: str, output_file: str) -> None:
    configs = parse_values(config_file)

    if not is_valid_data(configs, config_file):
        sys.exit(1)
    grid, entry, exit_, directions, stamp42 = parse_maze_file(output_file)

    expected_rows = configs["HEIGHT"]
    expected_cols = configs["WIDTH"]
    wrong_cols = any(len(row) != expected_cols for row in grid)
    if len(grid) != expected_rows or wrong_cols:
        print(f"Error: Grid dimensions dont match {config_file}")
        sys.exit(1)

    print(build_maze(grid, entry=configs["ENTRY"], exit_=configs["EXIT"],
                     stamp42=stamp42))


def render_solution(config_file: str,
                    output_file: str) -> list[tuple[int, int]]:
    import time
    configs = parse_values(config_file)

    if not is_valid_data(configs, config_file):
        sys.exit(1)

    grid, entry, exit_, directions, stamp42 = parse_maze_file(output_file)

    expected_rows = configs["HEIGHT"]
    expected_cols = configs["WIDTH"]
    wrong_cols = any(len(row) != expected_cols for row in grid)
    if len(grid) != expected_rows or wrong_cols:
        print(f"Error: Grid dimensions dont match {config_file}")
        sys.exit(1)

    ex, ey = entry
    path = get_path(directions, (ey, ex))

    for i in range(len(path)):
        partial_path = path[:i+1]

        print("\033[H\033[J", end="")

        print(build_maze(
            grid,
            entry=entry,
            exit_=exit_,
            stamp42=stamp42,
            path=partial_path
        ))

        time.sleep(0.02)
    return path
