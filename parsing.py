import sys
from typing import Any


def parse_values() -> dict[str, Any]:
    values: dict[str, Any] = {}
    try:
        with open("config.txt", "r") as file:
            for line in file:
                line = line.strip()

                # Ignorar comentários e linhas vazias
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, raw = line.split("=", 1)
                    key = key.strip()
                    raw = raw.strip()

                    # Converter tipos automaticamente
                    parsed: Any
                    if raw.lower() in ("true", "false"):
                        parsed = raw.lower() == "true"
                    elif "," in raw:  # coordenadas
                        parsed = tuple(map(int, raw.split(",")))
                    elif raw.isdigit():
                        parsed = int(raw)
                    else:
                        parsed = raw

                    values[key] = parsed
    except FileNotFoundError:
        print("Error: File Not Found")
    except IsADirectoryError:
        print("Output file cannot be dirctory")
        sys.exit(1)
    except Exception as err:
        print(err)
        sys.exit(1)
    return values


"""
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True

x axis = WIDTH
y axis = HEIGHT
"""


def is_valid_data(configs: dict[str, Any]) -> bool:
    width = configs["WIDTH"]
    height = configs["HEIGHT"]
    entry_row, entry_col = configs["ENTRY"]
    exit_row, exit_col = configs["EXIT"]
    if width <= 0:
        print("Invalid width.")
        return False
    if height <= 0:
        print("Invalid height.")
        return False
    if (entry_row < 0
        or entry_row > width
            or entry_col < 0
            or entry_col > height):
        print(f'Invalid entry coordinates. '
              f'Entry coordinates: {configs["ENTRY"]}')
        return False
    if (exit_row < 0
        or exit_row > width
            or exit_col < 0
            or exit_col > height):
        print(f"Invalid exit coordinates. "
              f"Exit coordinates: {configs['EXIT']}")
        return False
    return True


def print_data() -> None:
    if is_valid_data(parse_values()):
        configs = parse_values()
        for key, value in configs.items():
            if key == "ENTRY" or key == "EXIT":
                print(f"Max Values: X:{configs['HEIGHT']} "
                      f"Y:{configs['WIDTH']}")
            print(f"{key} : {value}")
            print()


if __name__ == "__main__":
    print_data()
