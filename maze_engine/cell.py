PSEUDOCODIGO: maze_engine/cell.py

OBJETIVO
- Definir a entidade Cell (celula individual do maze).

ESTRUTURA Cell
- x: inteiro
- y: inteiro
- walls: inteiro em bitmask (inicia com ALL_WALLS)
- visited: booleano (inicia False)
- parent: referencia para outra Cell ou nulo

METODOS
- has_wall(direction):
  devolver True se o bit da direcao estiver ativo

- remove_wall(direction):
  limpar bit da direcao em walls

- reset_search_state():
  visited = False
  parent = nulo
