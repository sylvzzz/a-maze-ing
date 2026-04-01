PSEUDOCODIGO: parsing.py

OBJETIVO
- Ler config.txt e transformar em estrutura de configuracao.
- Validar campos obrigatorios do projeto A-Maze-ing.

FUNCAO parse_values()
1. iniciar dicionario CONFIG_VAZIO
2. tentar abrir ficheiro config.txt
3. para cada LINHA no ficheiro:
   3.1 remover espacos nas pontas
   3.2 se linha vazia ou comecar por # -> continuar
   3.3 separar por '=' em CHAVE e VALOR
   3.4 normalizar CHAVE e VALOR
   3.5 converter VALOR:
       - se true/false -> booleano
       - se formato x,y -> tuplo de inteiros
       - se numero -> inteiro
       - senao -> texto
   3.6 guardar em CONFIG_VAZIO[CHAVE] = VALOR
4. tratar erros comuns:
   - ficheiro inexistente
   - permissao negada
   - valor invalido
5. devolver CONFIG_VAZIO

FUNCAO is_valid_data(CONFIG)
1. confirmar que WIDTH e HEIGHT existem e sao > 0
2. confirmar que ENTRY e EXIT existem no formato (x, y)
3. confirmar limites:
   - 0 <= entry_x < WIDTH
   - 0 <= entry_y < HEIGHT
   - 0 <= exit_x < WIDTH
   - 0 <= exit_y < HEIGHT
4. confirmar que OUTPUT_FILE existe ou usar default maze.txt
5. confirmar que PERFECT existe ou usar default True
6. devolver True se tudo valido, senao False

FLUXO MAIN (ALTO NIVEL)
1. configs = parse_values()
2. se is_valid_data(configs) for False -> terminar com erro
3. mostrar resumo dos parametros lidos
