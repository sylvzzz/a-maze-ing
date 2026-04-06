import sys
import os
from parsing import parse_values, is_valid_data


N, S, E, W = 0x8, 0x4, 0x2, 0x1


def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"


RESET = "\033[0m"

WALL = bg(220, 220, 220)
PASSAGE = bg(10, 10, 10)
ENTRY = bg(180, 0, 220)
EXIT = bg(200, 30, 30)


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
        print(f"Error: maze file '{path}' not found.")
        sys.exit(1)
    return grid


def render(grid: list[list[int]], entry: tuple, exit_: tuple) -> str:
    rows, cols = len(grid), len(grid[0])
    # ENTRY/EXIT from config are (col, row) i.e. (x, y) — convert to (row, col)
    entry_pos = (entry[1], entry[0])
    exit_pos = (exit_[1], exit_[0])
    out = []

    out.append(WALL + " " * (cols * 4 + 1) + RESET)

    for r in range(rows):
        row = WALL + " " + RESET
        for c in range(cols):
            cell = grid[r][c]
            if (r, c) == entry_pos:
                fill = ENTRY
            elif (r, c) == exit_pos:
                fill = EXIT
            else:
                fill = PASSAGE
            row += fill + "   " + RESET
            row += (WALL if cell & E else PASSAGE) + " " + RESET
        out.append(row)

        wall_row = WALL + " " + RESET
        for c in range(cols):
            wall_row += (
                (WALL if grid[r][c] & S else PASSAGE) + "   " + RESET
            )
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
    actual_rows = len(grid)
    actual_cols = len(grid[0]) if grid else 0

    if actual_rows != expected_rows or any(
        len(row) != expected_cols for row in grid
    ):
        print(
            f"Error: grid in '{output_file}' is "
            f"{actual_rows}x{actual_cols}, "
            f"expected {expected_rows}x{expected_cols}."
        )
        sys.exit(1)

    print(render(grid, entry=configs["ENTRY"], exit_=configs["EXIT"]))


if __name__ == "__main__":
    while True:
        os.system("clear")
        print("\n")
        main()
        print("\n")
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = int(input("Choice? (1-4): "))
        if choice == 4:
            break
