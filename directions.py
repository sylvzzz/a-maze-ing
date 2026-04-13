def print_directions(path: list) -> None:
    for direction in path:
        print(direction)


if __name__ == "__main__":
    path = ["S", "N","N","E","S"]
    print_directions(path)