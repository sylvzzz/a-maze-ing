PSEUDOCODIGO: main.py

OBJETIVO
- Ser o entrypoint principal do projeto (fora de maze_engine).
- Orquestrar ciclo completo: carregar config, validar, gerar maze, renderizar, interagir com utilizador.

FLUXO PRINCIPAL
1. carregar configuracao com parse_values()
2. validar configuracao com validate_config()
3. se invalida -> terminar com mensagem clara
4. chamar run_app(config)

FUNCAO run_app(config)
1. estado.show_path = False
2. estado.theme_index = 0
3. gerar maze inicial via facade de aplicacao
4. iniciar loop interativo:
   - limpar ecra
   - renderizar maze
   - mostrar menu
   - ler opcao
   - processar opcao
   - repetir ate sair

MENU
1 -> gerar novo maze
2 -> alternar mostrar caminho
3 -> alternar tema de cores
4 -> sair
