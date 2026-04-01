# 🧩 A-Maze-ing — Maze Engine Technical Design

## 📌 Overview

This document describes the full technical design of the **maze engine** component of the **A-Maze-ing** project.

The maze engine is responsible for:

* Representing the maze internally
* Generating the maze structure
* Solving the maze
* Encoding the maze into hexadecimal format
* Providing reusable logic via a `MazeGenerator` module

This document focuses **only on the algorithmic core**, not parsing or rendering.

---

# 🧠 Core Concepts

## Maze as a Graph

A maze is internally represented as a **grid graph**.

Each cell:

* is a **node**
* walls are **edges**
* open walls mean **connections**

This allows use of:

* Graph traversal algorithms
* Pathfinding algorithms

Main algorithms used:

* Recursive Backtracker (generation)
* Breadth-First Search (solving)

---

# 🧱 System Architecture

```text
Maze Engine
│
├── Structure
│     ├── Cell
│     ├── Maze
│     └── Directions
│
├── Generation
│     └── Recursive Backtracker
│
├── Solving
│     └── Breadth-First Search
│
├── Encoding
│     └── Hexadecimal Conversion
│
└── Utilities
```

---

# 📁 Folder Structure

```text
maze/
│
├── directions.py
├── cell.py
├── maze.py
│
├── generator.py
├── solver.py
├── encoder.py
│
└── utils.py
```

---

# 🧭 Module 1 — directions.py

## Purpose

Defines all directional logic used throughout the system.

This module contains **constants and mappings**, not classes.

---

## Directions

```text
N → North
E → East
S → South
W → West
```

---

## Movement Mapping

Defines coordinate offsets.

```text
N → (0, -1)
E → (1, 0)
S → (0, 1)
W → (-1, 0)
```

Used for:

* Finding neighbors
* Moving in the grid

---

## Opposite Directions

```text
N ↔ S
E ↔ W
```

Used when removing walls between cells.

---

## Bit Encoding

Each direction corresponds to a bit.

```text
N → 1
E → 2
S → 4
W → 8
```

Used during hexadecimal encoding.

---

# 🧱 Module 2 — cell.py

## Purpose

Represents a single maze cell.

---

## Cell Structure

```text
Cell
│
├── x : int
├── y : int
│
├── north : bool
├── east  : bool
├── south : bool
├── west  : bool
│
├── visited : bool
```

---

## Initial State

Every cell starts:

```text
north = True
east  = True
south = True
west  = True
visited = False
```

Meaning:

All walls are closed.

---

## Responsibilities

Each cell must:

* Track its walls
* Track visitation state
* Allow wall removal
* Provide wall state access

---

# 🧱 Module 3 — maze.py

## Purpose

Represents the full maze structure.

---

## Maze Structure

```text
Maze
│
├── width : int
├── height : int
│
├── grid : List[List[Cell]]
│
├── entry : (x,y)
├── exit  : (x,y)
│
├── seed : int | None
```

---

## Grid Representation

The grid is a 2D list.

```text
grid[y][x]
```

Example:

```text
WIDTH=4
HEIGHT=3

grid =

[
 [C C C C]
 [C C C C]
 [C C C C]
]
```

---

## Core Responsibilities

Maze must:

* Create the grid
* Validate coordinates
* Provide neighbors
* Remove walls
* Maintain maze consistency

---

## Core Methods

```text
create_grid()

get_cell(x, y)

is_inside(x, y)

get_neighbors(cell)

remove_wall(cell_a, cell_b)
```

---

# 🧠 Maze Generation

## Module: generator.py

Algorithm:

```text
Recursive Backtracker (DFS-based)
```

---

## Purpose

Generate a **perfect maze**.

Meaning:

* One unique path between any two cells
* Fully connected
* No isolated cells

---

## Algorithm Flow

```text
1. Start at entry cell
2. Mark visited
3. Push to stack

4. While stack not empty:

    Get unvisited neighbors

    If neighbors exist:
        Choose random neighbor
        Remove wall
        Mark visited
        Push neighbor

    Else:
        Pop stack (backtrack)
```

---

## Data Structures Used

```text
Stack
Visited flags
Random selection
```

---

# 🧠 Maze Solving

## Module: solver.py

Algorithm:

```text
Breadth-First Search (BFS)
```

---

## Purpose

Find:

```text
Shortest path
from entry to exit
```

---

## Algorithm Flow

```text
1. Create queue
2. Add entry cell
3. Mark visited

4. While queue not empty:

    Get next cell

    If exit found:
        Stop

    Add neighbors
    Store parent
```

---

## Path Reconstruction

```text
Exit → Entry
(reversed)

Converted to:

N E S W sequence
```

---

# 🧠 Maze Encoding

## Module: encoder.py

Purpose:

Convert maze into:

```text
Hexadecimal wall representation
```

---

## Bit System

```text
North → 1
East  → 2
South → 4
West  → 8
```

---

## Encoding Example

Walls:

```text
N=True
E=False
S=True
W=False
```

Value:

```text
1 + 4 = 5
```

Hex:

```text
"5"
```

---

## Output Structure

```text
HEX GRID

(empty line)

ENTRY
EXIT
PATH
```

---

# 🧠 Maze Solving Output

Example path:

```text
E E S S W N
```

Meaning:

```text
Move East
Move East
Move South
Move South
Move West
Move North
```

---

# 🧠 Randomness System

Maze generation must support:

```text
seed
```

This ensures:

```text
Same seed → Same maze
```

Important for:

* Debugging
* Testing
* Reproducibility

---

# 🧠 Perfect Maze Concept

A perfect maze means:

```text
Exactly one path between any two cells.
```

Properties:

```text
Connected
No loops
No isolated regions
```

Equivalent to:

```text
Spanning Tree
```

In graph theory.

---

# 🧠 Edge Cases

Must support:

```text
Small mazes
Entry near borders
Exit near borders
Single-path constraints
```

Must prevent:

```text
Invalid coordinates
Disconnected cells
Broken wall consistency
```

---

# 🧠 Performance Considerations

Maze generation complexity:

```text
O(N)
```

Where:

```text
N = number of cells
```

Maze solving complexity:

```text
O(N)
```

Encoding complexity:

```text
O(N)
```

Total system remains efficient.

---

# 🧠 Internal Workflow

```text
Create Maze
        ↓
Generate Maze
        ↓
Solve Maze
        ↓
Encode Maze
        ↓
Output
```

---

# 🧠 Testing Strategy

Recommended tests:

```text
Small maze
Medium maze
Large maze
Different seeds
Edge coordinates
Perfect=True
Perfect=False
```

---

# 🧠 Reusability Design

Final goal:

```text
MazeGenerator class
```

Reusable in future projects.

Must allow:

```text
Custom size
Custom seed
Custom entry/exit
```

---

# 🧠 Final Pipeline

```text
CONFIG
   ↓
Maze creation
   ↓
Maze generation
   ↓
Maze solving
   ↓
Maze encoding
   ↓
Output
```

---

# 🏁 End of Design Document
