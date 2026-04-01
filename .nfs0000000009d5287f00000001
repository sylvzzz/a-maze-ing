from typing import Optional


class Maze():
    def __init__(
            self,
            width: int,
            height: int,
            entry: dict[str, int],
            exit: dict[str, int],
            filename: str,
            perfect: bool,
            pattern: str,
            seed: Optional[int]
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[int]] = []
        self.path: str = ""
        self.draw_path: list[list[str | None]] = []
        self.wall_colors: list[str] = [
                "\033[0m",
                "\033[31m",
                "\033[32m",
                "\033[33m",
                "\033[34m",
                "\033[35m",
                "\033[36m"
            ]
        self.some_cl: list[str] = [
                "\033[48;5;95m",
                "\033[48;5;214m",
                "\033[48;5;82m",
                "\033[48;5;201m",
            ]
        self.path_colors: list[str] = [
                "\033[48;5;279m",
                "\033[48;5;129m",
                "\033[48;5;123m",
                "\033[48;5;58m",
                "\033[48;5;202m",
                "\033[48;5;59m",
            ]
        self.filename: str = filename
        self.perfect: bool = perfect
        self.pattern = pattern or '42'
        self.seed: Optional[int] = seed
        self.has_config_seed = seed is not None
        self.path_index: int = 0
        self.wall_index: int = 0
        self.another_ind: int = 0
        self.animating: bool = False
        self.algorithm: str = "dfs"
        self.curr_cell: Optional[tuple[int, int]] = None
        self.animation_speed = 0.03

    def parse_maze_values() -> dict:
        values: dict = {}

        with open("config.txt", "r") as file:
            for line in file:
                line = line.strip()

                # Ignores comments and empty lines
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    # Converts types automaticly
                    if value.lower() in ("true", "false"):
                        value = value.lower() == "true"
                    elif "," in value:  # split coordinates into ints
                        value = tuple(map(int, value.split(",")))
                    elif value.isdigit():
                        value = int(value)

                    values[key] = value

        return values

    def show_or_hide_path() -> None:
        """option n2 is for show/ hide path from exit to entry"""

    def rotate_maze_colors() -> None:
        """option n3 is for rotating maze colors"""


def generate_new_maze() -> None:
    """option n1 is for generating new maze"""


def main() -> None:
    pass


if __name__ == "__main__":
    main()
