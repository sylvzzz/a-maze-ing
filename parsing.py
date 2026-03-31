def parse_values() -> dict:
    with open("config.txt", "r") as file:
        contents = file.read()
        print(contents)


if __name__ == "__main__":
    parse_values()
