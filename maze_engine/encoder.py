PSEUDOCODIGO: maze_engine/encoder.py

OBJETIVO
- Converter Maze para formato hexadecimal e vice-versa.

ESTRUTURA MazeEncoder

METODO encode(maze)
1. pedir ao maze to_hex_string()
2. devolver texto final para guardar em ficheiro

METODO decode_lines(raw)
1. separar texto por linhas
2. ignorar linhas vazias
3. para cada token hexadecimal, converter para inteiro base 16
4. devolver matriz 2D de inteiros
