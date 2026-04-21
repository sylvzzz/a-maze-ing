# maze_engine — Reusable Maze Generation Module

## Overview

`maze_engine` is the core engine responsible for maze creation, solving, and encoding in the A-Maze-ing project. It was designed as a fully standalone, importable Python package so that future projects can reuse the maze generation logic without depending on the main application.

The module exposes five main classes:

| Class | Role |
|---|---|
| `Cell` | Represents a single cell in the maze grid |
| `Maze` | Holds the grid, entry/exit points, and the "42" stamp |
| `MazeGenerator` | Generates the maze using a randomised DFS (recursive backtracker) |
| `MazeSolver` | Solves the maze using BFS to find the shortest path |
| `MazeEncoder` | Encodes the maze into the hex output format |
| `MazePipeline` | Convenience class that chains all steps together |

---

## Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

Or from source (requires `build`):

```bash
pip install build
python3 -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

---

## Quick Start

### Using the pipeline (recommended)

The simplest way to generate, solve and encode a maze in one go:

```python
from maze_engine import MazePipeline

pipeline = MazePipeline(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    output_file="maze.txt"
)

path = pipeline.run()
print("Solution path:", "".join(path))
```

`pipeline.run()` generates the maze, solves it, writes the encoded output to `output_file`, and returns the solution path as a list of direction strings (`"N"`, `"E"`, `"S"`, `"W"`).

---

## Step-by-step Usage

If you need more control over each stage, you can use the classes individually.

### 1. Create a Maze

```python
from maze_engine import Maze

maze = Maze(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True   # True = single path; False = multiple paths (loops allowed)
)
```

### 2. Generate the Maze

```python
from maze_engine import MazeGenerator

generator = MazeGenerator(maze, seed=42)  # seed is optional; omit for random
generator.generate()
```

The generator uses a **randomised depth-first search (recursive backtracker)**. It also:
- Embeds the "42" pattern by pre-marking those cells as visited so the DFS never carves through them.
- Opens exactly one border wall at the entry and one at the exit.
- When `perfect=False`, adds a controlled number of extra wall openings (~5% of total cells) while preventing any open area larger than 2×2 cells.

### 3. Solve the Maze

```python
from maze_engine import MazeSolver

solver = MazeSolver(maze)
path = solver.solve()   # returns list[str], e.g. ["S", "S", "E", "E", "N", ...]
```

The solver uses **BFS (breadth-first search)** starting from `maze.entry` to guarantee the shortest path to `maze.exit`. The result is a list of direction characters.

### 4. Encode and Write to File

```python
from maze_engine import MazeEncoder

encoder = MazeEncoder(maze, path)
encoded_text = encoder.encode()

with open("maze.txt", "w") as f:
    f.write(encoded_text)
```

---

## Custom Parameters

### MazePipeline

```python
MazePipeline(
    width: int,           # number of columns
    height: int,          # number of rows
    entry: tuple[int, int],
    exit: tuple[int, int],   # defaults to (width-1, height-1)
    perfect: bool,        # True = perfect maze, False = maze with loops
    output_file: str      # path to write the encoded output
)
```

### MazeGenerator

```python
MazeGenerator(
    maze: Maze,
    seed: int | None      # integer seed for reproducibility; None = random
)
```

---

## Accessing the Maze Structure

After generation, the `Maze` object exposes:

```python
maze.width          # int — number of columns
maze.height         # int — number of rows
maze.entry          # tuple[int, int] — (x, y) of the entry cell
maze.exit           # tuple[int, int] — (x, y) of the exit cell
maze.perfect        # bool
maze.stamp42        # set[tuple[int, int]] — coords of the "42" pattern cells
maze.grid           # list[list[Cell]] — the full 2D grid, accessed as grid[y][x]
```

### Accessing a Cell

```python
cell = maze.get_cell(x, y)   # returns Cell | None

cell.x, cell.y       # coordinates
cell.north           # bool — True means wall is present
cell.east
cell.south
cell.west
cell.visited         # bool — used during generation

cell.has_wall("N")   # True if north wall is present; accepts "N", "E", "S", "W"
cell.get_walls()     # dict[str, bool] — all four walls at once
```

### Accessing the Solution

```python
solver = MazeSolver(maze)
path = solver.solve()     # list[str] — shortest path as direction characters
# e.g. ["S", "E", "E", "S", "W", "S"]
```

You can also access it after the fact via `solver.path`.

---

## Output File Format

The encoder writes one hexadecimal character per cell. Each hex digit encodes the wall state using bitwise flags:

| Bit | Direction | Value |
|-----|-----------|-------|
| 0 (LSB) | North | 1 |
| 1 | East | 2 |
| 2 | South | 4 |
| 3 | West | 8 |

A wall being **closed** sets the bit to `1`; open means `0`.

**Example:** hex `F` (binary `1111`) = all four walls closed. Hex `6` (binary `0110`) = East and South walls closed, North and West open.

After the grid rows, a blank line separates the metadata:

```
<hex grid rows, one per line>

<entry_x>,<entry_y>
<exit_x>,<exit_y>
<solution path string, e.g. SSEENWW...>
<42 stamp coords, semicolon-separated as y,x pairs>
```

---

## Algorithm: Randomised DFS (Recursive Backtracker)

The generator uses a depth-first search that starts at the entry cell and carves paths by removing walls between unvisited neighbours, chosen in random order. Backtracking occurs when all neighbours of the current cell have already been visited.

This algorithm was chosen because:
- It produces mazes with a natural, winding feel and long dead-ends, which are visually interesting.
- It maps cleanly onto a recursive implementation with no complex data structures.
- It trivially produces **perfect mazes** (a spanning tree of the grid), and can be extended to add loops by reopening a small number of walls afterwards.
- Reproducibility is built in by seeding Python's `random` module before generation.

For **imperfect mazes** (`perfect=False`), after the DFS the generator iterates over shuffled cells and selectively removes extra walls — skipping any candidate that would create a 3×3 (or larger) open area, checked by `_has_open_area`.

---

## The "42" Pattern

Before generation, `maze.embed_42()` pre-marks a set of cells as visited according to a scaled pattern (small, medium, or large depending on maze dimensions). The DFS never carves through these cells, leaving them as fully-walled blocks that together form the visible "42" logo. The pattern coordinates are stored in `maze.stamp42`.

If the maze is too small to fit the pattern, a message is printed and generation continues without it.

---

## Example: Full Custom Flow

```python
from maze_engine import Maze, MazeGenerator, MazeSolver, MazeEncoder

# Build maze
maze = Maze(width=30, height=20, entry=(0, 0), exit=(29, 19), perfect=False)

# Generate with a fixed seed for reproducibility
gen = MazeGenerator(maze, seed=1337)
gen.generate()

# Solve
solver = MazeSolver(maze)
path = solver.solve()
print(f"Shortest path length: {len(path)} steps")

# Encode
encoder = MazeEncoder(maze, path)
output = encoder.encode()

with open("my_maze.txt", "w") as f:
    f.write(output)

# Inspect individual cells
for y in range(maze.height):
    for x in range(maze.width):
        cell = maze.get_cell(x, y)
        if cell and cell.has_wall("S"):
            pass  # south wall is present at this cell
```