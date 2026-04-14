
import random
from .maze import Maze
from .cell import Cell
from .directions import DIRECTIONS, MOVES, OPPOSITE


class MazeGenerator:
    def __init__(self, maze: Maze, seed: int) -> None:
        self.maze = maze
        self.seed = seed

    def generate(self) -> None:
        random.seed(self.seed)
        self.maze.embed_42()

        start_x, start_y = self.maze.entry
        start_cell = self.maze.get_cell(start_x, start_y)
        assert start_cell is not None
        self._dfs(start_cell)
        self.maze.open_borders()
        if not self.maze.perfect:
            self._open_extra_walls()

    def _dfs(self, current: Cell) -> None:
        current.mark_visited()

        neighbors = self.maze.get_neighbors(current)
        available = [(dir, neighbor) for (dir, neighbor) in neighbors
                     if neighbor.visited is False]
        random.shuffle(available)

        for (dir, neighbor) in available:
            if neighbor.visited is True:
                continue
            self.maze.break_wall(current, neighbor)
            self._dfs(neighbor)

    def _has_open_area(self, x: int, y: int) -> bool:
        for dy in [-2, -1, 0]:
            for dx in [-2, -1, 0]:
                top_x = x + dx
                top_y = y + dy
                if (
                    top_x < 0
                    or top_y < 0
                    or top_x + 2 > self.maze.width
                    or top_y + 2 > self.maze.height
                ):
                    continue
                is_open = True
                for by in range(3):
                    for bx in range(3):
                        cx = top_x + bx
                        cy = top_y + by
                        cell = self.maze.get_cell(cx, cy)
                        if cell is None:
                            is_open = False
                            continue
                        if bx < 2:
                            if cell.has_wall("E"):
                                is_open = False
                        if by < 2:
                            if cell.has_wall("S"):
                                is_open = False
                if is_open is True:
                    return True

        return False

    def _open_extra_walls(self) -> None:
        cells_maze: list[Cell] = []

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                current_cell = self.maze.get_cell(x, y)
                if current_cell is not None:
                    cells_maze.append(current_cell)

        random.shuffle(cells_maze)

        for cell in cells_maze:
            if (cell.x, cell.y) in self.maze.stamp42:
                continue
            for direction in DIRECTIONS:
                if not cell.has_wall(direction):
                    continue
                dx, dy = MOVES[direction]
                nx = cell.x + dx
                ny = cell.y + dy
                neighbor = self.maze.get_cell(nx, ny)
                if neighbor is None:
                    continue
                cell.remove_wall(direction)
                neighbor.remove_wall(OPPOSITE[direction])
                if self._has_open_area(cell.x, cell.y):
                    cell.add_wall(direction)
                    neighbor.add_wall(OPPOSITE[direction])
