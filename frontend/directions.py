def direction_to_coordinates(direction: str,
                             current: tuple[int, int]) -> tuple[int, int]:
    row, col = current
    if direction == "S":
        return (row + 1, col)
    elif direction == "N":
        return (row - 1, col)
    elif direction == "E":
        return (row, col + 1)
    elif direction == "W":
        return (row, col - 1)
    else:
        print("Unknown direction...")
        return (row, col)


def print_directions(path: list[str]) -> None:
    for direction in path:
        print(direction)


def get_path(directions: list[str],
             entry: tuple[int, int]) -> list[tuple[int, int]]:
    resolution: list[tuple[int, int]] = [entry]
    current = entry

    for direction in directions:
        current = direction_to_coordinates(direction, current)
        resolution.append(current)

    return resolution
