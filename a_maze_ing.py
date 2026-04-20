import sys
import os
import frontend as ui
import maze_engine as engine
from typing import Any
import time


def show_themes() -> None:
    print("\n" + "=" * 50)
    print("\nAvailable themes:")
    for i, name in enumerate(ui.theme_names):
        marker = " <-- current" if i == ui.theme_index else ""
        print(f"  {i + 1}. {name}{marker}")


def show_menu() -> None:
    current_theme_name = ui.theme_names[ui.theme_index]
    print("\n" + "=" * 55)
    print(f"Theme: {current_theme_name}")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path")
    print("3. Rotate colors")
    print("4. Re-generate a new maze and solve it")
    print("5. Re-generate a new maze with new theme")
    print("6. Re-generate a new maze with new theme and solve it")
    print("7. Show themes")
    print("8. Quit")


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    args = sys.argv
    if len(args) == 2:
        config_file = args[1]
        configs: dict[str, Any] = ui.parse_values(config_file)
        if ui.is_valid_data(configs, config_file):
            configs = {k.lower(): v for k, v in configs.items()}
            maze = engine.MazePipeline(**configs)
            maze.run()
            ui.render_maze(config_file, configs["output_file"])
            show_menu()
            path_is_showing = False
            while True:
                try:
                    choice = int(input("Choice? (1-8): "))
                    if choice == 1:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        path_is_showing = False
                        maze = engine.MazePipeline(**configs)
                        maze.run()
                        ui.render_maze(config_file, configs["output_file"])
                        show_menu()
                    elif choice == 2:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        if path_is_showing is False:
                            ui.render_solution(config_file,
                                               configs["output_file"])
                            path_is_showing = True
                        elif path_is_showing is True:
                            ui.render_maze(config_file, configs["output_file"])
                            path_is_showing = False
                        show_menu()
                    elif choice == 3:
                        path_is_showing = False
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ui.theme_index += 1
                        ui.theme_index %= len(ui.theme_names)
                        ui.render_maze(config_file, configs["output_file"])
                        show_menu()
                    elif choice == 4:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        maze = engine.MazePipeline(**configs)
                        maze.run()
                        ui.render_maze(config_file, configs["output_file"])
                        ui.render_solution(config_file,
                                           configs["output_file"])
                        show_menu()
                        path_is_showing = True
                    elif choice == 5:
                        path_is_showing = False
                        path_is_showing = False
                        maze = engine.MazePipeline(**configs)
                        maze.run()
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ui.theme_index += 1
                        ui.theme_index %= len(ui.theme_names)
                        ui.render_maze(config_file, configs["output_file"])
                        show_menu()
                    elif choice == 6:
                        path_is_showing = False
                        path_is_showing = False
                        maze = engine.MazePipeline(**configs)
                        maze.run()
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ui.theme_index += 1
                        ui.theme_index %= len(ui.theme_names)
                        ui.render_maze(config_file, configs["output_file"])
                        ui.render_solution(config_file,
                                           configs["output_file"])
                        show_menu()
                    elif choice == 7:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        show_themes()
                        input("\nPress any key to go back...")
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ui.render_maze(config_file, configs["output_file"])
                        show_menu()
                    elif choice == 67:
                        path_is_showing = False
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Segmentation fault (core dumped)")
                        time.sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("SHUT THE F*** UP PLEASE!")
                        time.sleep(2)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ui.render_maze(config_file, configs["output_file"])
                        show_menu()
                    elif choice == 42:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("#include <stdio.h>")
                        print("\nint main()")
                        print("{")
                        print('     char *student1 = "dbotelho";')
                        print('     char *student2 = "gguia-ma";')
                        print('     printf("The best a-maze-ing'
                              ' was made by: %s and %s", student1, student2);')
                        print('     return 0;')
                        print('}')
                        time.sleep(3)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("$ cc -Wall -Wextra -Werror a-maze-ing.c")
                        time.sleep(3)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("$ ./a-maze-ing")
                        print("Segmentation fault (core dumped)")
                        time.sleep(3)
                        os.system('cls' if os.name == 'nt' else 'clear')
                        input("Press if piscine python gave yu nightmares...")
                        path_is_showing = False
                        os.system('cls' if os.name == 'nt' else 'clear')
                        ui.render_maze(config_file, configs["output_file"])
                        show_menu()
                    elif choice == 8:
                        break
                    else:
                        print("Please enter a valid choice (1-8)...")
                except ValueError:
                    print("Please enter a number between 1-8...")
                except EOFError:
                    break
    elif len(args) > 2:
        print("Too many arguments. Usage: python3 a_maze_ing.py config.txt")
    elif len(args) < 2:
        print("Too few arguments. Usage: python3 a_maze_ing.py config.txt")
