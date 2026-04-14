# 🧩 Maze Hexadecimal Encoding Guide

## 🧱 Cell Encoding (Hex → Walls)

Each cell of the maze is represented by a **single hexadecimal digit (0–F)**.  
This digit encodes which walls are **closed (1)** or **open (0)** using bits.

| Hex | Binary | North (N) | East (E) | South (S) | West (W) | Meaning |
|-----|--------|----------|----------|----------|----------|---------|
| 0   | 0000   | 0        | 0        | 0        | 0        | No walls |
| 1   | 0001   | 1        | 0        | 0        | 0        | North wall |
| 2   | 0010   | 0        | 1        | 0        | 0        | East wall |
| 3   | 0011   | 1        | 1        | 0        | 0        | North + East |
| 4   | 0100   | 0        | 0        | 1        | 0        | South wall |
| 5   | 0101   | 1        | 0        | 1        | 0        | North + South |
| 6   | 0110   | 0        | 1        | 1        | 0        | East + South |
| 7   | 0111   | 1        | 1        | 1        | 0        | North + East + South |
| 8   | 1000   | 0        | 0        | 0        | 1        | West wall |
| 9   | 1001   | 1        | 0        | 0        | 1        | North + West |
| A   | 1010   | 0        | 1        | 0        | 1        | East + West |
| B   | 1011   | 1        | 1        | 0        | 1        | North + East + West |
| C   | 1100   | 0        | 0        | 1        | 1        | South + West |
| D   | 1101   | 1        | 0        | 1        | 1        | North + South + West |
| E   | 1110   | 0        | 1        | 1        | 1        | East + South + West |
| F   | 1111   | 1        | 1        | 1        | 1        | All walls closed |

---

## 🧠 Bit Mapping

| Bit Position | Value | Direction |
|-------------|------|----------|
| 0 (LSB)     | 1    | North    |
| 1           | 2    | East     |
| 2           | 4    | South    |
| 3           | 8    | West     |

- **1 = wall closed 🚧**
- **0 = wall open 🚪**

---