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
        exit: tuple[int, int],
        perfect: bool = True,
        output_file: str = "maze.txt",
    ) -> None:
        if exit is None:
            exit = (width - 1, height - 1)
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.output_file = output_file
        # create maze
        self.maze = Maze(width, height, entry, exit, perfect)
        # create path
        self.path: list[str] = []

    def write_to_file(self, text: str) -> None:
        with open(self.output_file, "w") as file:
            file.write(text)

    def run(self) -> list[str]:
        # generate Maze
        generator = MazeGenerator(self.maze)
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
