import sys
from typing import Any


def parse_values(config_file: str) -> dict[str, Any]:
    values: dict[str, Any] = {}
    try:
        with open(config_file, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, raw = line.split("=", 1)
                    key = key.strip()
                    raw = raw.strip()

                    parsed: Any
                    if raw.lower() in ("true", "false"):
                        parsed = raw.lower() == "true"
                    elif "," in raw:
                        parsed = tuple(map(int, raw.split(",")))
                    elif raw.lstrip("-").isdigit():
                        parsed = int(raw)
                    else:
                        parsed = raw

                    values[key] = parsed
    except ValueError:
        print(f"Invalid values, Check {config_file}...")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: {config_file} File Not Found")
        sys.exit(1)
    except IsADirectoryError:
        print(f"Config file ({config_file}/) cannot be dirctory")
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
OUTPUT_FILE=
PERFECT=True

x axis = WIDTH
y axis = HEIGHT
"""


def whats_missing(configs: dict[str, Any], config_file: str) -> None:
    try:
        configs["WIDTH"]
    except KeyError:
        print(f"Missing WIDTH in {config_file}")

    try:
        configs["HEIGHT"]
    except KeyError:
        print(f"Missing HEIGHT in {config_file}")

    try:
        configs["ENTRY"]
    except KeyError:
        print(f"Missing ENTRY in {config_file}")

    try:
        configs["EXIT"]
    except KeyError:
        print(f"Missing EXIT in {config_file}")

    try:
        configs["OUTPUT_FILE"]
    except KeyError:
        print(f"Missing OUTPUT_FILE in {config_file}")

    try:
        configs["PERFECT"]
    except KeyError:
        print(f"Missing PERFECT in {config_file}")


def is_valid_data(configs: dict[str, Any], config_file: str) -> bool:
    try:
        width = configs["WIDTH"]
        height = configs["HEIGHT"]
        is_perfect = configs["PERFECT"]
        output_file = configs["OUTPUT_FILE"]
        entry_col, entry_row = configs["ENTRY"]
        exit_col, exit_row = configs["EXIT"]
        if width <= 0:
            print(f"Invalid width. Width processed: {width}")
            return False
        if height <= 0:
            print(f"Invalid height. Height processed: {height}")
            return False
        if (entry_row < 0
                or entry_row >= height
                or entry_col < 0
                or entry_col >= width):
            print(f'Invalid entry coordinates. '
                  f'Entry coordinates: {configs["ENTRY"]}')
            return False
        if (exit_row < 0
                or exit_row >= height
                or exit_col < 0
                or exit_col >= width):
            print(f"Invalid exit coordinates. "
                  f"Exit coordinates: {configs['EXIT']}")
            return False
        if is_perfect is not True and is_perfect is not False:
            print("Configuration (PERFECT) isnt True neither false...")
            return False
        if not isinstance(output_file, str) or output_file.strip() == "":
            print(f"Invalid OUTPUT_FILE in {config_file}: empty value")
            return False
    except ValueError:
        whats_missing(configs, config_file)
        print(f"Invalid values, Check {config_file}...")
        sys.exit(1)
    except FileNotFoundError:
        whats_missing(configs, config_file)
        print(f"File {config_file} not found...")
        sys.exit(1)
    except TypeError:
        whats_missing(configs, config_file)
        print(f"Invalid values, Check {config_file}...")
        sys.exit(1)
    except KeyError:
        whats_missing(configs, config_file)
        sys.exit(1)
    return True


def print_data(config_file: str) -> None:
    if is_valid_data(parse_values(config_file), config_file):
        configs = parse_values(config_file)
        for key, value in configs.items():
            if key == "ENTRY" or key == "EXIT":
                print(f"Max Values: X:{configs['HEIGHT']} "
                      f"Y:{configs['WIDTH']}")
            print(f"{key} : {value}")
            print()
        print(configs)


if __name__ == "__main__":
    print_data(sys.argv[1])
