PSEUDOCODIGO: maze_engine/solver.py

OBJETIVO
- Resolver maze com BFS e devolver caminho minimo entry -> exit.

ESTRUTURA MazeSolver
- recebe Maze

METODO solve()
1. reset_search_state no maze
2. start = celula entry
3. goal = celula exit
4. queue = [start]
5. start.visited = True

6. enquanto queue nao vazia:
   6.1 current = remover primeiro da queue
   6.2 se current == goal:
       devolver caminho reconstruido por parent
   6.3 para cada direcao cardinal:
       - se existir parede nessa direcao, ignorar
       - obter neighbor por delta
       - se neighbor valido e nao visitado:
         marcar visited
         neighbor.parent = current
         adicionar neighbor na queue

7. se goal nunca encontrado: devolver lista vazia

METODO _rebuild_path(goal)
1. path = []
2. current = goal
3. enquanto current existe:
   adicionar (current.x, current.y)
   current = current.parent
4. inverter path
5. devolver path

METODO solve_as_directions()
1. converter caminho de coordenadas para sequencia N/E/S/W
2. devolver lista de direcoes
