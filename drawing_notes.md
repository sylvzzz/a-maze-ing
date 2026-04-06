# 🧩 Guia de Estudo — Renderização de Labirintos em Terminal (Python)

> Baseado no código `display.py` — entenda cada técnica usada para desenhar o labirinto e o símbolo "42" no terminal.
---

## 📚 Índice

1. [Representação do Labirinto com Bitmask](#1-representação-do-labirinto-com-bitmask)
2. [Cores ANSI no Terminal](#2-cores-ansi-no-terminal)
3. [Lógica de Renderização (linha a linha)](#3-lógica-de-renderização-linha-a-linha)
4. [Pixel Art — O símbolo "42"](#4-pixel-art--o-símbolo-42)
5. [Continuidade Visual entre Células](#5-continuidade-visual-entre-células)
6. [Fluxo Geral do Programa](#6-fluxo-geral-do-programa)
7. [Exercícios para Praticar](#7-exercícios-para-praticar)
8. [Ideias para Melhorar o Código](#8-ideias-para-melhorar-o-código)

---

## 1. Representação do Labirinto com Bitmask

O labirinto é armazenado como uma **grade de inteiros hexadecimais**. Cada célula guarda quais paredes estão **abertas** (passagem) usando um **bitmask** (máscara de bits):

```python
N, S, E, W = 0x8, 0x4, 0x2, 0x1
#            1000  0100  0010  0001  (binário)
```

| Direção | Hex  | Binário |
|---------|------|---------|
| Norte   | `0x8`| `1000`  |
| Sul     | `0x4`| `0100`  |
| Leste   | `0x2`| `0010`  |
| Oeste   | `0x1`| `0001`  |

### Como verificar se uma parede está aberta?

```python
# Usando o operador AND bit a bit (&)
if cell & E:          # a parede leste está aberta?
    east_wall = PASSAGE   # sim → passagem (cor clara)
else:
    east_wall = WALL      # não → parede (cor escura)
```

### Exemplo prático

```
Célula com valor 0x6 = 0110 em binário
  bit S (0100) → ligado → parede Sul está aberta
  bit E (0010) → ligado → parede Leste está aberta
  bit N (1000) → desligado → parede Norte está fechada
  bit W (0001) → desligado → parede Oeste está fechada
```

### 💡 Por que usar bitmask?

- Compacto: 4 direções em apenas 4 bits (1 byte)
- Rápido: verificação com uma única operação `&`
- Simples de serializar: salva/carrega como hex no arquivo

---

## 2. Cores ANSI no Terminal

O terminal suporta **escape codes ANSI** para colorir o fundo e o texto. O código usa cores RGB de 24 bits:

```python
def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

RESET = "\033[0m"  # reseta a cor para o padrão
```

### Estrutura do escape code

```
\033[  48  ;  2  ;  R  ;  G  ;  B  m
  │    │    │      │    │    │
  │    │    │      └────┴────┴── valores RGB (0-255)
  │    │    └── modo true color (24-bit)
  │    └── 48 = cor de fundo | 38 = cor do texto
  └── ESC (caractere de escape)
```

### Paleta de cores usada

```python
WALL    = bg(10,  10,  10)   # quase preto  → paredes fechadas
PASSAGE = bg(220, 220, 220)  # cinza claro  → passagens abertas
ENTRY   = bg(180, 0,   220)  # roxo         → entrada do labirinto
EXIT    = bg(200, 30,  30)   # vermelho      → saída do labirinto
PATH    = bg(255, 255, 0)    # amarelo       → caminho solução
SYMBOL  = bg(100, 180, 255)  # azul claro    → símbolo "42"
```

### Como a cor é aplicada

```python
# Cada "célula" no terminal ocupa 3 espaços em branco
row += color + "   " + RESET
#              ^^^
#              espaços coloridos — a cor de fundo
#              cria o efeito visual de "bloco"
```

---

## 3. Lógica de Renderização (linha a linha)

Para cada linha `r` do grid, **duas linhas de terminal** são impressas:

```
┌─────────────────────────────────────────┐
│  render_cell_row(r, ...)                │  ← corpo da célula + parede leste
│  render_wall_row(r, ...)                │  ← parede sul da célula
│  render_cell_row(r+1, ...)              │
│  render_wall_row(r+1, ...)              │
│  ...                                    │
└─────────────────────────────────────────┘
```

### render_cell_row — linha principal

```python
def render_cell_row(r, grid, entry_pos, exit_pos, path):
    row = PASSAGE + " " + RESET   # borda esquerda

    for c, cell in enumerate(grid[r]):
        color = pick_cell_color(r, c, ...)   # cor da célula
        char  = pick_cell_char(r, c, path)   # conteúdo (" * " ou "   ")

        # Verifica a parede leste
        if cell & E:
            east_wall = PASSAGE   # aberta
        else:
            east_wall = WALL      # fechada

        row += color + char + RESET       # célula (3 chars)
        row += east_wall + " " + RESET    # separador leste (1 char)

    return row
```

### render_wall_row — parede sul

```python
def render_wall_row(r, grid):
    row = PASSAGE + " " + RESET   # borda esquerda

    for c, cell in enumerate(grid[r]):
        if cell & S:
            south_wall = PASSAGE   # parede sul aberta
        else:
            south_wall = WALL      # parede sul fechada

        row += south_wall + "   " + RESET   # 3 chars da parede sul
        row += PASSAGE + " " + RESET        # separador (canto)

    return row
```

### Visualização do resultado para 2x2 células

```
╔═══════════════════╗
║ [C1]│[C2]│        ← render_cell_row (linha 0)
║─────┼─────        ← render_wall_row (linha 0)
║ [C3]│[C4]│        ← render_cell_row (linha 1)
║─────┼─────        ← render_wall_row (linha 1)
╚═══════════════════╝
```

---

## 4. Pixel Art — O símbolo "42"

O "42" é desenhado como **pixel art hardcoded**: um conjunto de coordenadas `(linha, coluna)` que correspondem a células do grid que devem ser coloridas de azul.

```python
SYMBOL_CELLS = set([
    # Número "4" — haste esquerda
    (2, 3), (3, 3), (4, 3),

    # Número "4" — haste direita (altura total)
    (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6),

    # Número "4" — barra horizontal
    (4, 3), (4, 4), (4, 5), (4, 6),

    # Número "2" — barra superior
    (2, 9), (2, 10), (2, 11),

    # Número "2" — vertical superior direita
    (3, 11),

    # Número "2" — barra do meio
    (4, 9), (4, 10), (4, 11),

    # Número "2" — vertical inferior esquerda
    (5, 9), (6, 9), (7, 9),

    # Número "2" — barra inferior
    (8, 9), (8, 10), (8, 11),
])
```

### Visualização do "42" no grid (. = vazio, X = célula azul)

```
col:  0  1  2  3  4  5  6  7  8  9  10 11
row2:          X  .  .  X        X  X  X
row3:          X  .  .  X        .  .  X
row4:          X  X  X  X        X  X  X
row5:          .  .  .  X        X  .  .
row6:          .  .  .  X        X  .  .
row7:          .  .  .  X        X  .  .
row8:          .  .  .  X        X  X  X
```

### Como a cor é aplicada

```python
def is_symbol(r, c):
    return (r, c) in SYMBOL_CELLS   # O(1) — lookup em set

def pick_cell_color(r, c, entry_pos, exit_pos, path):
    if is_entry(r, c, entry_pos): return ENTRY
    if is_exit(r, c, exit_pos):   return EXIT
    if is_on_path(r, c, path):    return PATH
    if is_symbol(r, c):           return SYMBOL  # ← aqui
    return WALL
```

> **Prioridade:** Entrada > Saída > Caminho > Símbolo > Parede padrão
---

## 5. Continuidade Visual entre Células

Sem tratamento especial, as **paredes entre células do símbolo** teriam a cor padrão (escura), quebrando o visual do "42". A solução é colorir também as paredes entre células adjacentes do símbolo:

```python
# Parede leste (render_cell_row)
east_neighbor_is_symbol = is_symbol(r, c) and is_symbol(r, c + 1)
if east_neighbor_is_symbol:
    east_wall = SYMBOL   # preenche a lacuna horizontal

# Parede sul (render_wall_row)
south_neighbor_is_symbol = is_symbol(r, c) and is_symbol(r + 1, c)
if south_neighbor_is_symbol:
    south_wall = SYMBOL  # preenche a lacuna vertical
```

### Antes vs Depois

```
Antes (sem tratamento):     Depois (com tratamento):
[azul]|[azul]               [azul][azul]
       ^ parede escura              ^ parede azul (contínua)
```

---

## 6. Fluxo Geral do Programa

```
run()
 │
 ├── load_config()        → lê configurações (WIDTH, HEIGHT, ENTRY, EXIT, etc.)
 │
 ├── load_maze()          → lê o arquivo maze.txt
 │    └── load_grid()     → converte cada valor hex para int
 │
 └── loop principal:
      │
      ├── display_maze()       → renderiza o labirinto
      │    └── render_maze()
      │         ├── render_top_border()
      │         ├── render_cell_row()  × N linhas
      │         └── render_wall_row()  × N linhas
      │
      └── display_menu()       → mostra opções ao usuário
           ├── 1 → regenerate
           ├── 2 → show/hide path
           ├── 3 → rotate colors (TODO)
           └── 4 → quit
```

---

## 7. Exercícios para Praticar

### Nível 1 — Compreensão

1. O que representa o valor `0xF` em uma célula? Quais paredes estão abertas?
2. O que acontece se `WALL` e `PASSAGE` tiverem cores muito parecidas?
3. Por que `SYMBOL_CELLS` é um `set` em vez de uma `list`?

### Nível 2 — Modificação

4. Adicione um novo símbolo ao labirinto (ex: as letras "AB" ou um coração ♥).
5. Implemente a função `handle_rotate_colors()` que troca as cores de `WALL` e `PASSAGE`.
6. Faça o caminho (`PATH`) piscar no terminal usando escape codes de animação.

### Nível 3 — Expansão

7. Implemente um **solver BFS** para encontrar o caminho real da entrada até a saída.
8. Adicione suporte a **múltiplos temas de cor** (claro, escuro, monocromático).
9. Salve o labirinto renderizado como uma **imagem PNG** usando a biblioteca Pillow.

---

## 8. Ideias para Melhorar o Código

| Melhoria | Descrição |
|----------|-----------|
| **Solver real** | Substituir o `hardcoded_path` por BFS/DFS/A* |
| **Gerador de labirinto** | Implementar algoritmos como Recursive Backtracker ou Prim's |
| **Animação** | Mostrar a geração/solução célula a célula com `time.sleep()` |
| **Configuração de símbolos** | Ler o pixel art de um arquivo externo |
| **Testes unitários** | Testar `render_cell_row`, `pick_cell_color`, `is_symbol`, etc. |
| **Múltiplos caminhos** | Encontrar e comparar todos os caminhos possíveis |
| **Interface com setas** | Navegar pelo labirinto em tempo real com input do teclado |

---

## 📖 Referências Rápidas

```python
# Operações de bitmask
cell & N   # norte está aberto?
cell & S   # sul está aberto?
cell & E   # leste está aberto?
cell & W   # oeste está aberto?

# Escape codes ANSI
"\033[48;2;R;G;Bm"   # cor de fundo RGB
"\033[38;2;R;G;Bm"   # cor de texto RGB
"\033[0m"            # reset

# Set lookup — O(1)
(r, c) in SYMBOL_CELLS

# Conversão de coordenadas
# configs usa (col, row) = (x, y)
entry_pos = (entry[1], entry[0])  # converte para (row, col)
```

---