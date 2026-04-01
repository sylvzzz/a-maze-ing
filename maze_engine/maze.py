PSEUDOCODIGO: maze_engine/maze.py

OBJETIVO
- Representar a grelha completa do labirinto.

ESTRUTURA Maze
- width, height
- entry, exit
- seed opcional
- grid: lista 2D de Cell

INICIALIZACAO
1. guardar parametros
2. criar grid com height linhas e width colunas
3. em cada posicao criar Cell(x, y)

METODOS
- is_inside(x, y):
  devolver True se coordenada dentro dos limites

- get_cell(x, y):
  se fora dos limites -> nulo
  senao -> grid[y][x]

- get_neighbors(cell, only_unvisited=False):
  para cada direcao em CARDINAL_DIRECTIONS:
    calcular (nx, ny)
    obter vizinho com get_cell
    se existir e condicao de visited permitir -> adicionar
  devolver lista de (neighbor, direction)

- remove_wall_between(first, second, direction):
  remover parede de first na direction
  remover parede de second na direcao oposta

- reset_search_state():
  percorrer todas as celulas e limpar visited/parent

- to_hex_lines():
  converter cada celula para 1 digito hexadecimal
  devolver linhas separadas por espaco

- to_hex_string():
  juntar linhas com quebra de linha
