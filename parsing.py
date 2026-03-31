def parse_values() -> dict:
    values = {}

    with open("config.txt", "r") as file:
        for line in file:
            line = line.strip()

            # Ignorar comentários e linhas vazias
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                # Converter tipos automaticamente
                if value.lower() in ("true", "false"):
                    value = value.lower() == "true"
                elif "," in value:  # coordenadas
                    value = tuple(map(int, value.split(",")))
                elif value.isdigit():
                    value = int(value)

                values[key] = value

    return values


if __name__ == "__main__":
    configs = parse_values()
    for key, value in configs.items():
        print(f"{key} : {value}")
        print()
