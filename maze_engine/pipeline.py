from .maze import Maze
from .generator import MazeGenerator
from .solver import MazeSolver
from .encoder import MazeEncoder


class MazePipeline:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int] | None = None,
        perfect: bool = True,
    ) -> None:
        if exit is None:
            exit = (width - 1, height - 1)
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        # create maze
        self.maze = Maze(width, height, entry, exit, perfect)
        # create path
        self.path: list[str] = []

    def write_to_file(self, text: str) -> None:
        with open("maze.txt", "w") as file:
            file.write(text)

    def run(self) -> list[str]:
        # generate Maze
        generator = MazeGenerator(self.maze, seed=42)
        generator.generate()

        # solve Maze
        solver = MazeSolver(self.maze)
        self.path = solver.solve()

        # encode the maze
        encoder = MazeEncoder(self.maze, self.path)
        encoded_text = encoder.encode()

        # create maze.txt
        self.write_to_file(encoded_text)

        return self.path
