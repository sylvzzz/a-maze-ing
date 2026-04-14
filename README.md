*This project has been created as part of the 42 curriculum by dbotelho and gguia-ma.*

---

# A-Maze-ing

> A maze generated in hexadecimal represented on the terminal via a `.txt` file with its properties and configs. A grid of hex values, an entry, an exit, a path, and the 42 logo, stamped in cell.


```
293953D11579515553D3
AAAA9696E93C3AD5543A
C6AAC3A956C56C5513C2
93AAD46A97955553EABA
AEAC3950696D517A9686
C3C3AAFAFAFFFA96ABC3
943AC6FEF857FAA96A96
AD6C53FFFAFFFAAA946B
851796D3FAFD506AA93A
87A9693AFAFFFA96AAAA
E92A96C2D2D53C6BC6C2
96EC693C3C3945385396
851556C7C56853EC3C6B
C3C53939157ABA956D12
D457C6C6C5546C455568

0,0
19,14
SSENNESSSSSESSEESWSWSSENENESESESEENWNNNNNNNENEEEEESSWSSSWSSENENNNENNENNWWWWNNEEEESESESSWSESWSWWSSSENNESSESWSWNWWSESWWSEEEENES
```

---

## Description

`A-Maze-ing` is a terminal-based maze generator and solver written in Python. It generates random mazes using depth-first search (recursive backtracker) to generate the maze, solves them via breadth-first search, and renders everything in your terminal with ASCII. There are multiple themes, a solution path you can toggle on and off, and — as a nod to 42 School — the number "42" is always stamped somewhere in the middle of the maze, made of blocked cells you can't walk through.

The project is split into a backend (generation, solving, encoding) and a frontend (rendering, themes, user interaction) and a middleware (parsing from files). The backend is also reusable as a module to future projects that will need maze generation, for example Pac-Man (Milestone 4)

---

## Instructions

### Requirements

- Python 3.10 or later
- No external dependencies needed(standard library only)

### Installation

```bash
# clone the repo
git clone git@github.com:sylvzzz/a-maze-ing.git a-maze-ing
cd a-maze-ing

# (optional but recommended) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies (if any are listed)
make install
```

### Running

```bash
python3 a_maze_ing.py config.txt
```

Or via the Makefile:

```bash
make run       # run with default config
make debug     # run with pdb debugger
make lint      # flake8 + mypy checks
make clean     # remove __pycache__, .mypy_cache, etc.
```

### Makefile targets

| Target | Description |
|--------|-------------|
| `install` | Install project dependencies |
| `run` | Run the main script |
| `debug` | Run with Python's built-in debugger (pdb) |
| `clean` | Remove caches and temp files |
| `lint` | Run `flake8` and `mypy` with required flags |
| `lint-strict` | Run `mypy --strict` (optional) |

---

## Configuration file format

The program takes a single config file as argument. Each line is a `KEY=VALUE` pair. Lines starting with `#` are ignored.

```ini
# example config.txt
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42           # optional — set for reproducible mazes
```

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `WIDTH` | int | Number of columns | `WIDTH=20` |
| `HEIGHT` | int | Number of rows | `HEIGHT=15` |
| `ENTRY` | x,y | Entry cell coordinates | `ENTRY=0,0` |
| `EXIT` | x,y | Exit cell coordinates | `EXIT=19,14` |
| `OUTPUT_FILE` | str | Where to write the maze | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | bool | Single path between entry and exit | `PERFECT=True` |
| `SEED` | int | Optional seed for reproducibility | `SEED=12345` |

A default `config.txt` is included at the root of the repository.

---

## Maze generation algorithm

The algorithm used is **recursive DFS** (also known as the recursive backtracker).

It works like this: start from the entry cell, mark it as visited, then randomly pick an unvisited neighbor, break the wall between them, and recurse. When you hit a dead end, backtrack until you find a cell with unvisited neighbors. Repeat until all cells are visited.

Before the DFS runs, the "42" shape is stamped into the grid — those cells are pre-marked as visited so the DFS skips them entirely, leaving them as solid blocked regions.

If `PERFECT=False`, a second pass removes extra walls without creating open 2×2 areas, adding loops to the maze.

### Why this algorithm?

Recursive DFS was the right fit for this project for a few reasons. It's simple to reason about — the call stack is the frontier, so there are no extra data structures to manage. It produces long, winding corridors which look visually interesting in a terminal renderer. It integrates naturally with the "42" stamp: cells that are pre-marked visited are simply skipped by the DFS, so the pattern embeds without any special casing. And it's easy to make reproducible with a seed, which the subject requires.

Alternatives like Prim's or Kruskal's would produce different visual textures (more branchy, more uniform), but DFS gives the maze that classic labyrinthine feel.

---

## Output file format

```
<hex grid>      — HEIGHT lines, each with WIDTH hex chars, no separators
                — blank line
<ex>,<ey>       — entry position (col, row)
<xx>,<xy>       — exit position (col, row)
<directions>    — solution path as a string of N/S/E/W characters
```

Each cell's walls are encoded as a 4-bit hex value:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 (MSB) | West |

`1` means the wall is closed, `0` means open. Example: `A` (binary `1010`) = East and West walls closed.

---

## Visual representation

The maze is rendered in the terminal using ANSI 24-bit background colors. Each cell is 3 characters wide with 1-character separators. Colors come from a theme dict and can be cycled at runtime.

```
====================
Theme: Ocean
1. Re-generate a new maze
2. Show/Hide path
3. Rotate colors
4. Quit
Choice? (1-4):
```

The "42" cells are rendered in the theme's `number` color — a distinct shade from the walls and passages, so the pattern is always visible.

### Themes

Themes live in `frontend/themes.py`. Each one is a dict of ASCII background codes:

| Key | Colors |
|-----|--------|
| `wall` | Maze walls |
| `passage` | Open corridors |
| `entry` | Start cell |
| `exit` | End cell |
| `number` | The 42 stamp |
| `path` | Solution path overlay |

Adding a new theme is just adding an entry to `THEMES` using the `bg(r, g, b)` function.

---

## Reusable module — `mazegen`

The maze generation logic is packaged as a standalone pip-installable module at the root of the repository: `mazegen-1.0.0-py3-none-any.whl` (and `.tar.gz`).

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Building from source

```bash
pip install build
python3 -m build
# outputs dist/mazegen-1.0.0-py3-none-any.whl and dist/mazegen-1.0.0.tar.gz
```


## Project structure

```
.
├── a_maze_ing.py            # entry point
├── config.txt               # default configuration
├── Makefile
├── mazegen-1.0.0-py3-none-any.whl   # installable package
├── pyproject.toml           # package build config
├── backend/
│   ├── maze.py              # Maze class — grid, stamp42, neighbors, walls
│   ├── cell.py              # Cell class — individual tile with wall state
│   ├── generator.py         # MazeGenerator — DFS + optional wall removal
│   ├── solver.py            # MazeSolver — finds the solution path
│   ├── encoder.py           # MazeEncoder — serializes maze to .txt format
│   ├── pipeline.py          # MazePipeline — orchestrates the whole flow
│   └── directions.py        # direction constants, moves, opposites
└── frontend/
    ├── __init__.py          # theme state, build_maze, render functions
    ├── themes.py            # color themes (Default, Ocean, Earthy, ...)
    ├── parsing.py           # config file parser and validator
    └── directions.py        # get_path — reconstructs cell coords from directions
```

---

## Team and project management

### Roles

| Member | Responsibilities |
|--------|-----------------|
| dbotelho | Frontend — ASCII renderer, themes, UI/UX and parsing |
| gguia-ma | Backend — maze generation, solver and encoder |

### Planning

We started by mapping out the data flow: config → maze → file → render. The first week focused on getting the DFS generator and file format right. The second week was the frontend and the 42 stamp rendering. The last stretch was fixing edge cases — the coordinate axis swap between internal `(x, y)` and file `(row, col)`, the `stamp42` not being written to the output file, and theme colors for the 42 pattern not showing up due to an undefined variable.

### What worked well

The pipeline architecture (`MazePipeline`) made it easy to swap out pieces independently — we could test the encoder without touching the renderer, and vice versa. Separating `backend` and `frontend` into distinct packages kept things clean and made the reusable module straightforward to extract.

### What could be improved

The coordinate convention (`(x, y)` internally, `(row, col)` in the file) caused subtle bugs that took a while to track down. A single canonical coordinate type throughout would have saved time. The 42 stamp position is currently always centered — it could be randomized within a safe margin for more variety.

### Tools used

- `mypy` for static type checking
- `flake8` for style linting
- `pytest` for unit tests (not submitted)
- `build` for packaging the `mazegen` module
- Claude (Anthropic) — see Resources below

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Jamis Buck's Maze Algorithms](http://www.jamisbuck.org/mazes/) — excellent visual breakdowns of DFS, Prim's, Kruskal's and more
- [Recursive Backtracker — Think Labyrinth](https://www.astrolog.org/labyrnth/algrithm.htm)
- [Python `typing` module docs](https://docs.python.org/3/library/typing.html)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)

### AI usage

Claude (Anthropic) was used during this project for the following tasks:

- **Debugging the `stamp42` pipeline** — the coords were stored as `(x, y)` internally but the encoder was either not writing them at all (missing line in `encode()`) or writing them in the wrong order, causing the 42 to render as an empty set or rotated 90°. Claude helped trace the bug through the encoder → file → renderer chain by inspecting each step in sequence.
- **Fixing a `NameError` in the renderer** — `NUMBER_WALL` was referenced in `build_maze` but never defined; Claude identified the undefined variable and suggested replacing both occurrences with the already-defined `NUMBER`.
- **Generating the README structure**, which was then reviewed, corrected, and filled in with project-specific content.

All AI-generated content was reviewed, understood, and tested before being included in the project.

---

## A note on the 42 coordinate swap

If you ever touch `embed_42()` or the encoder, keep this in mind: `stamp42` internally stores `(x, y)` = `(col, row)`, but the maze file stores them as `(row, col)`. The encoder handles the swap explicitly:

```python
# in MazeEncoder.encode()
result += ";".join(f"{y},{x}" for x, y in sorted(self.maze.stamp42)) + "\n"
```

If you write `x, y` directly, the 42 will render rotated 90°. Don't ask how we know.

---

## Known quirks

- The terminal needs to support true color for themes to look right. If everything appears gray, your terminal may not support 24-bit ANSI codes.
- Very small mazes (roughly under 10×8) may not fit the 42 pattern — the program prints a warning and continues without it.
- The solution path is computed once at generation time and doesn't update if the maze file is manually edited.