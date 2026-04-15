from . import directions


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False

    def remove_wall(self, direction: str) -> None:
        if direction == directions.N:
            self.north = False
        elif direction == directions.E:
            self.east = False
        elif direction == directions.S:
            self.south = False
        elif direction == directions.W:
            self.west = False
        else:
            raise ValueError("Invalid direction")

    def add_wall(self, direction: str) -> None:
        if direction == directions.N:
            self.north = True
        elif direction == directions.E:
            self.east = True
        elif direction == directions.S:
            self.south = True
        elif direction == directions.W:
            self.west = True
        else:
            raise ValueError("Invalid direction")

    def has_wall(self, direction: str) -> bool:
        if direction == directions.N:
            return self.north
        elif direction == directions.E:
            return self.east
        elif direction == directions.S:
            return self.south
        elif direction == directions.W:
            return self.west
        else:
            raise ValueError("Invalid direction")

    def mark_visited(self) -> None:
        if self.visited is False:
            self.visited = True

    def reset_visited(self) -> None:
        if self.visited is True:
            self.visited = False

    def get_walls(self) -> dict[str, bool]:
        return {
            directions.N: self.north,
            directions.E: self.east,
            directions.S: self.south,
            directions.W: self.west
        }
