from .directions import BIT_VALUES, DIRECTIONS
from .maze import Maze
from .cell import Cell
import sys


class MazeEncoder:
    def __init__(self, maze: Maze, path: list[str]) -> None:
        self.maze = maze
        self.path = path

    def _cell_to_hex(self, cell: Cell) -> str:
        value = 0

        for direction in DIRECTIONS:
            if cell.has_wall(direction):
                value += BIT_VALUES[direction]
        return hex(value)[2:].upper()

    def _check_stamp42(self) -> None:
        entry = self.maze.entry
        exit_ = self.maze.exit
        stamp42 = self.maze.stamp42

        if entry in stamp42:
            print(f"Entry coordinates {entry} cannot be in 42 logo")
            sys.exit(1)
        if exit_ in stamp42:
            print(f"Exit coordinates {exit_} cannot be in 42 logo")
            sys.exit(1)

    def encode(self) -> str:
        self._check_stamp42()
        result = ""
        # grid
        for y in range(self.maze.height):
            line = ""
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)
                assert cell is not None
                hex_value = self._cell_to_hex(cell)
                line += hex_value
            result += line + "\n"

        result += "\n"

        # entry
        ex, ey = self.maze.entry
        result += f"{ex},{ey}\n"

        # exit
        xx, xy = self.maze.exit
        result += f"{xx},{xy}\n"

        # path
        result += "".join(self.path) + "\n"

        result += ";".join(f"{y},{x}"
                           for x, y in sorted(self.maze.stamp42)) + "\n"

        return result
