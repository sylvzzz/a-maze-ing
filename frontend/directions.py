from frontend.parsing import parse_values


def direction_to_coordinates(path: str, config_file: str) -> tuple:
    configs = parse_values(config_file)
    entry = configs["ENTRY"]
    if path == "S":
        print("Moving south")
        return (entry[1], entry[0] + 1)
    elif path == "N":
        print("Moving north")
        return (entry[1], entry[0] - 1)
    elif path == "E":
        print("Moving east")
        return (entry[1] + 1, entry[0])
    elif path == "W":
        print("Moving west")
        return (entry[1], entry[0] - 1)


def print_directions(path: list) -> None:
    for direction in path:
        print(direction)


def get_path(config_file: str) -> None:
    with open(config_file) as file:
        try:
            content: str = file.read()
            directions: list = list(content)
        except FileNotFoundError:
            print("File not found...")
            return
    resolution: list[tuple[int, int]] = []
    # print_directions(path)
    print("Printing path and transforming it to coordinates\n")
    for direction in directions:
        resolution.append(direction_to_coordinates(direction, config_file))
    print("\nResolution coordinates: ", resolution)


if __name__ == "__main__":
    get_path()
