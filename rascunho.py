PSEUDOCODIGO: rascunho.py (UI terminal)

OBJETIVO
- Mostrar o maze no terminal em modo visual.
- Permitir gerar novo maze, alternar caminho e mudar tema de cor.

CONSTANTES
- BITS DE PAREDE: N=8, E=2, S=4, W=1
- PALETAS DE CORES: WALL, PASSAGE, ENTRY, EXIT, PATH

FUNCAO parse_grid(caminho)
1. abrir ficheiro de saida do maze
2. ler linha a linha
3. ignorar linhas vazias
4. converter cada valor hexadecimal para inteiro
5. devolver matriz 2D

FUNCAO render(grid, entry, exit, path, show_path)
1. converter entry/exit de (x,y) para indices de matriz
2. criar conjunto de posicoes do caminho se show_path=True
3. desenhar moldura superior
4. para cada linha da grelha:
   4.1 desenhar interior das celulas
   4.2 colorir entry, exit, path ou passagem normal
   4.3 desenhar paredes verticais conforme bit E
   4.4 desenhar linha de paredes horizontais conforme bit S
5. devolver string final a imprimir

FUNCAO build_and_render(configs, path, show_path)
1. ler ficheiro OUTPUT_FILE
2. validar dimensoes da grelha contra WIDTH/HEIGHT
3. chamar render(...)
4. devolver representacao textual

FUNCAO main()
1. carregar configs e validar
2. gerar maze inicial com pipeline do motor
3. iniciar loop de menu:
   - opcao 1: gerar maze novo
   - opcao 2: mostrar/esconder caminho
   - opcao 3: trocar tema de cores
   - opcao 4: sair
4. limpar ecra e re-renderizar a cada acao
