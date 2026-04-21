from typing import Optional
from .cell import Cell
from .directions import DIRECTIONS, MOVES, OPPOSITE


class Maze:
    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit: tuple[int, int], perfect: bool) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.stamp42: set[tuple[int, int]] = set()
        self.omitted_42 = False

    def is_within_bounds(self, x: int, y: int) -> bool:
        if (0 <= y < self.height) and (0 <= x < self.width):
            return True
        return False

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if self.is_within_bounds(x, y) is True:
            return self.grid[y][x]
        return None

    def get_neighbors(self, current_cell: Cell) -> list[tuple[str, Cell]]:
        found_neighbors = list()
        for direction in DIRECTIONS:
            nx = current_cell.x + MOVES[direction][0]
            ny = current_cell.y + MOVES[direction][1]
            neighbor = self.get_cell(nx, ny)
            if neighbor is not None:
                found_neighbors.append((direction, neighbor))
        return found_neighbors

    def break_wall(self, current_cell: Cell, neighbor: Cell) -> None:
        if neighbor.x > current_cell.x:
            direction = "E"
        elif neighbor.x < current_cell.x:
            direction = "W"
        elif neighbor.y > current_cell.y:
            direction = "S"
        elif neighbor.y < current_cell.y:
            direction = "N"
        else:
            raise ValueError("Cells are not neighbors")
        current_cell.remove_wall(direction)
        neighbor.remove_wall(OPPOSITE[direction])

    def restore_wall(self, current_cell: Cell, neighbor: Cell) -> None:
        if neighbor.x > current_cell.x:
            direction = "E"
        elif neighbor.x < current_cell.x:
            direction = "W"
        elif neighbor.y > current_cell.y:
            direction = "S"
        elif neighbor.y < current_cell.y:
            direction = "N"
        else:
            raise ValueError("Cells are not neighbors")
        current_cell.add_wall(direction)
        neighbor.add_wall(OPPOSITE[direction])

    def _get_42_coords(self) -> set[tuple[int, int]]:
        pat_small = [
            "#.#.###",
            "#.#...#",
            "###.###",
            "..#.#..",
            "..#.###",
        ]

        pat_med = [
            "#..#.####",
            "#..#....#",
            "####.####",
            "...#.#...",
            "...#.####",
        ]

        pat_big = [
            "#...#.#####",
            "#...#.....#",
            "#...#.....#",
            "#####.#####",
            "....#.#....",
            "....#.#....",
            "....#.#####",
        ]

        if self.width < 28 or self.height < 20:
            pattern = pat_small
        elif self.width < 45 or self.height < 30:
            pattern = pat_med
        else:
            pattern = pat_big

        base_h = len(pattern)
        base_w = len(pattern[0])

        margin = 2
        avail_w = self.width - (2 * margin)
        avail_h = self.height - (2 * margin)

        if avail_w < base_w or avail_h < base_h:
            raise ValueError("Maze too small for 42 pattern")

        ox = (self.width - base_w) // 2
        oy = (self.height - base_h) // 2

        coords: set[tuple[int, int]] = set()

        for py in range(base_h):
            row = pattern[py]
            for px in range(base_w):
                if row[px] == ".":
                    # '.' means empty — no stamping at this position
                    continue
                coords.add((ox + px, oy + py))

        return coords

    def stamp_42(self, coords: set[tuple[int, int]]) -> None:
        self.stamp42 = coords
        for (x, y) in coords:
            cell = self.get_cell(x, y)
            if cell is not None:
                cell.mark_visited()

    def embed_42(self) -> None:
        self.omitted_42 = False
        try:
            coords = self._get_42_coords()
            self.stamp_42(coords)
        except ValueError:
            self.omitted_42 = True
            print("Maze too small for 42 pattern")
