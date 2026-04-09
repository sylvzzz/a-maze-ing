import sys
import os
from typing import List, Tuple
import frontend as ui
Path = List[Tuple[int, int]]


def show_menu(config_file: str) -> None:
    current_theme_name = ui.theme_names[ui.theme_index]
    ui.render_maze(config_file)
    print("\n" + "=" * 20)
    print(f"Theme: {current_theme_name}")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path")
    print("3. Rotate colors")
    print("4. Quit")


def show_path(grid: List[List[int]], path: Path) -> str:
    """Render maze with a highlighted path."""
    rows = len(grid)
    cols = len(grid[0])

    t = ui.get_theme()
    wall = t["wall"]
    passage = t["passage"]

    path_color = ui.bg(0, 0, 255)  # azul

    out: List[str] = []

    out.append(wall + " " * (cols * 4 + 1) + ui.RESET)

    for r in range(rows):
        row = wall + " " + ui.RESET

        for c in range(cols):
            fill = path_color if (r, c) in path else passage

            row += fill + "   " + ui.RESET

            has_east_wall = bool(grid[r][c] & ui.E)
            row += (wall if has_east_wall else passage) + " " + ui.RESET

        out.append(row)

        wall_row = wall + " " + ui.RESET
        for c in range(cols):
            has_south_wall = bool(grid[r][c] & ui.S)
            color = wall if has_south_wall else passage

            wall_row += color + "   " + ui.RESET
            wall_row += wall + " " + ui.RESET

        out.append(wall_row)

    return "\n".join(out)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        config_file = args[1]
        os.system('cls' if os.name == 'nt' else 'clear')
        show_menu(config_file)
        while True:
            try:
                choice = int(input("Choice? (1-4): "))
                if choice == 1:
                    print("Option (1. Re-generate a new maze) selected")
                elif choice == 2:
                    # print("Option (2. Show/Hide path) selected")
                    grid = ui.parse_grid("maze.txt")
                    path = [
                        (0, 0), (1, 0), (2, 0), (3, 0),
                        (3, 1), (3, 2), (4, 2), (5, 2),
                        (6, 2), (7, 2), (8, 2), (9, 2),
                        (10, 2), (11, 2), (12, 2), (13, 2),
                        (14, 2), (14, 3), (14, 4), (14, 5),
                    ]

                    print(show_path(grid, path))
                elif choice == 3:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    ui.theme_index = (ui.theme_index + 1) % len(ui.theme_names)
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
