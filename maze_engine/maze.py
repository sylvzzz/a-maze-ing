from typing import Optional
import cell
from .directions import DIRECTIONS, MOVES, OPPOSITE

class Maze:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.grid = [[cell.Cell(x, y) for x in range(width)] for y in range(height)]]

    def is_within_bonds(self, x: int, y: int) -> bool:
        if (0 <= y < self.height) and (0 <= x < self.width):
            return True
        return False
    
    def get_cell(self, x: int, y: int) -> Optional[cell.Cell]:
        if self.is_within_bonds(x, y) is True:
            return self.grid[y][x]
        return None

    def get_neighbors(self, current_cell: cell.Cell) -> list[tuple[str, cell.Cell]]:
        found_neighbors = list()
        for direction in DIRECTIONS:
            nx = current_cell.x + MOVES[direction][0]
            ny = current_cell.y + MOVES[direction][1]
            neighbor = self.get_cell(nx, ny)
            if neighbor is not None:
                found_neighbors.append((direction, neighbor))
        return found_neighbors

    def break_wall(self, current_cell: cell.Cell, neighbor: cell.Cell) -> None:
        if neighbor.x > current_cell.x:
            direction = "E"
        elif neighbor.x < current_cell.x:
            direction = "W"
        elif neighbor.y > current_cell.y:
            direction = "S"
        elif neighbor.y < current_cell.y:
            direction = "N"
        current_cell.remove_wall(direction)
        neighbor.remove_wall(OPPOSITE[direction])