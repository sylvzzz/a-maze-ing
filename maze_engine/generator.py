PSEUDOCODIGO: maze_engine/generator.py

OBJETIVO
- Gerar maze com Recursive Backtracker (DFS com stack).

ESTRUTURA MazeGenerator
- recebe Maze
- usa RNG com seed do Maze para reproducibilidade

METODO generate()
1. reset_search_state no maze
2. start = celula da entrada
3. marcar start.visited = True
4. stack = [start]

5. enquanto stack nao vazia:
   5.1 current = topo da stack
   5.2 neighbors = vizinhos nao visitados de current
   5.3 se neighbors vazia:
       - pop da stack (backtrack)
       - continuar
   5.4 escolher neighbor aleatorio
   5.5 remover paredes entre current e neighbor
   5.6 marcar neighbor.visited = True
   5.7 push neighbor na stack

6. fim: maze conectado e sem ciclos (maze perfeito)
