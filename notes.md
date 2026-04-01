Boa pergunta! Aqui está um roadmap claro do que estudar e por onde começar:

---

## 🗺️ Roadmap — Maze Generator & Solver em Python (ASCII Terminal)

---

### 1. Parsing do Config File
**O que ver:** `open()`, `str.strip()`, `str.partition()`, `str.startswith()`
**Conceitos:** ler ficheiro linha a linha, ignorar comentários (`#`), separar `KEY=VALUE`, tratar erros com `try/except` e exceções customizadas (`class ConfigError(Exception)`)

---

### 2. Validação dos Parâmetros
**O que ver:** type casting (`int()`, `bool()`), condições de validação
**Conceitos:** verificar que WIDTH/HEIGHT são inteiros positivos, que ENTRY/EXIT estão dentro dos limites da grelha, que PERFECT é `True` ou `False`

---

### 3. Estrutura de Dados do Maze
**O que ver:** listas 2D em Python (`[[...] for _ in range(n)]`), dicionários, conjuntos (`set`)
**Conceitos:** representar o labirinto como uma grelha de células, cada célula com paredes (Norte, Sul, Este, Oeste)

---

### 4. Geração do Maze
**O que ver:** algoritmos de geração de labirintos
**Conceitos a pesquisar:**
- **Recursive Backtracker (DFS)** — mais simples, bom ponto de partida
- **Kruskal's / Prim's** — para mazes perfeitos alternativos
- A diferença entre **maze perfeito** (sem ciclos, sempre há caminho único) e **imperfeito**

---

### 5. Representação ASCII
**O que ver:** `print()`, strings com `+`, `join()`, caracteres como `█`, `|`, `-`, `+`, ` `
**Conceitos:** converter a grelha de células+paredes para linhas de texto, linha a linha, célula a célula — é aqui que entra o teu trabalho principal

---

### 6. Output para Ficheiro
**O que ver:** `open()` com modo `"w"`, `file.write()`
**Conceitos:** escrever o maze em ASCII para o ficheiro definido em `OUTPUT_FILE`

---

### 7. Resolução do Maze
**O que ver:** algoritmos de pathfinding
**Conceitos a pesquisar:**
- **BFS (Breadth-First Search)** — garante caminho mais curto, fácil de implementar
- **DFS** — mais simples mas não garante caminho ótimo
- Marcar o caminho solução no ASCII (ex: com `·` ou `*`)

---

### 8. Display no Terminal
**O que ver:** `os.system('clear')`, biblioteca `colorama` (opcional, para cores)
**Conceitos:** imprimir o maze limpo no terminal, destacar ENTRY, EXIT e solução

---

## 📌 Por onde começar?

```
1. config parser  →  2. validação  →  3. estrutura da grelha
       →  4. geração (DFS)  →  5. render ASCII  →  6. output ficheiro
```

Começa pelo **passo 1 e 2** — são independentes e dão-te a base. Depois o **passo 3 e 5** juntos, porque a forma como representas o maze em memória define diretamente como o renderizas em ASCII.

---

**Dica principal:** pesquisa *"recursive backtracker maze python"* e *"maze ASCII representation python"* — há muitos exemplos visuais que tornam os conceitos muito mais claros.


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

## 🔁 Wall Consistency Rules

Adjacent cells must agree on shared walls:

- If a cell has **East wall (E)** → right neighbor must have **West wall (W)**
- If a cell has **South wall (S)** → bottom neighbor must have **North wall (N)**

❌ Invalid example:
- Cell A has East wall
- Cell B (to the right) has no West wall

---

## 📍 Coordinates

- Format: **(column, row)** → `(x, y)`
- In code (matrix access):
  ```python
  (row, col) = (y, x)