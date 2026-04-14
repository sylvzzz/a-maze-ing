
from .maze import Maze
from collections import deque


class MazeSolver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.path: list[str] = []

    def _bfs(self) -> dict[tuple[int, int],
                           tuple[tuple[int, int], str] | None]:
        start_x, start_y = self.maze.entry

        start_cell = self.maze.get_cell(*self.maze.entry)
        assert start_cell is not None

        line = deque([start_cell])

        parents: dict[
            tuple[int, int],
            tuple[tuple[int, int], str] | None
        ] = {(start_x, start_y): None}

        while line:
            current = line.popleft()
            assert current is not None

            if (current.x, current.y) == self.maze.exit:
                break

            for direction, neighbor in self.maze.get_neighbors(current):
                if current.has_wall(direction):
                    continue
                if (neighbor.x, neighbor.y) in parents:
                    continue

                parents[(neighbor.x, neighbor.y)] = (
                    (current.x, current.y),
                    direction,
                )
                line.append(neighbor)

        return parents

    def solve(self) -> list[str]:
        parents = self._bfs()
        path = []
        current = self.maze.exit

        while current in parents:
            parent = parents[current]
            if parent is None:
                break

            parent_coords, direction = parent
            path.append(direction)
            current = parent_coords

        path.reverse()
        self.path = path
        return self.path
