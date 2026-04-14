import sys
import os
import frontend as ui
import maze_engine as engine

# output_file = configs.get("OUTPUT_FILE", "maze.txt")


def show_menu() -> None:
    current_theme_name = ui.theme_names[ui.theme_index]
    print("\n" + "=" * 20)
    print(f"Theme: {current_theme_name}")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path")
    print("3. Rotate colors")
    print("4. Quit")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    args = sys.argv
    if len(args) == 2:
        config_file = args[1]
        configs: dict = ui.parse_values(config_file)
        configs = {k.lower(): v for k, v in configs.items()}
        maze = engine.MazePipeline(**configs)
        maze.run()
        ui.render_maze(config_file, "maze.txt")
        show_menu()
        path_is_showing = False
        while True:
            try:
                choice = int(input("Choice? (1-4): "))
                if choice == 1:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    path_is_showing = False
                    maze = engine.MazePipeline(**configs)
                    maze.run()
                    ui.render_maze(config_file, "maze.txt")
                    show_menu()
                elif choice == 2:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if path_is_showing is False:
                        ui.render_solution(config_file, "maze.txt")
                        path_is_showing = True
                    elif path_is_showing is True:
                        ui.render_maze(config_file, "maze.txt")
                        path_is_showing = False
                    show_menu()
                elif choice == 3:
                    path_is_showing = False
                    os.system('cls' if os.name == 'nt' else 'clear')
                    ui.theme_index = (ui.theme_index + 1) % len(ui.theme_names)
                    ui.render_maze(config_file, "maze.txt")
                    show_menu()
                elif choice == 4:
                    break
                else:
                    print("Please enter a valid choice (1-4)...")
            except ValueError:
                print("Please enter a number between 1-4...")
            except EOFError:
                break
    elif len(args) > 2:
        print("Too many arguments. Usage: python3 a_maze_ing.py config.txt")
    elif len(args) < 2:
        print("Too few arguments. Usage: python3 a_maze_ing.py config.txt")
