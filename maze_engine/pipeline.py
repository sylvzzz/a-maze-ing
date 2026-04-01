PSEUDOCODIGO: maze_engine/pipeline.py

OBJETIVO
- Orquestrar pipeline completo: criar, gerar, resolver e guardar.

FUNCAO build_maze_from_config(config)
1. maze = Maze(width, height, entry, exit, seed)
2. MazeGenerator(maze).generate()
3. path = MazeSolver(maze).solve()
4. devolver (maze, path)

FUNCAO save_maze_file(maze, output_file)
1. raw = MazeEncoder.encode(maze)
2. escrever raw no ficheiro output_file

FUNCAO generate_and_save(config)
1. (maze, path) = build_maze_from_config(config)
2. save_maze_file(maze, OUTPUT_FILE)
3. devolver (maze, path)
