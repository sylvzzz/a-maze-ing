# Maze Renderer — Documentação do Código

## Visão Geral

Este script Python renderiza um labirinto no terminal usando cores ANSI de 24 bits. O labirinto é lido a partir de um ficheiro de texto, e o script sobrepõe o número **"42"** no centro do labirinto como decoração visual. O utilizador pode depois interagir através de um menu simples.

---

## Dependências e Imports

```python
import sys
import os
from parsing import parse_values, is_valid_data
```

- `sys` — usado para terminar o programa com `sys.exit()` em caso de erro.
- `os` — importado mas não usado diretamente no ficheiro.
- `parsing` — módulo externo (não incluído aqui) que fornece `parse_values()` e `is_valid_data()` para ler e validar o ficheiro de configuração.

---

## Constantes

### Direções (Bitmask)

```python
N, S, E, W = 0x8, 0x4, 0x2, 0x1
```

Cada célula do labirinto é representada por um inteiro hexadecimal. Cada bit indica se existe uma **parede** numa direção:

| Constante | Valor | Direção |
|-----------|-------|---------|
| `N`       | `0x8` | Norte   |
| `S`       | `0x4` | Sul     |
| `E`       | `0x2` | Este    |
| `W`       | `0x1` | Oeste   |

Por exemplo, um valor `0xF` (1111 em binário) significa paredes em todas as direções.

### Cores ANSI

```python
def bg(r, g, b):
    return f"\033[48;2;{r};{g};{b}m"

RESET = "\033[0m"
```

A função `bg()` gera um código de escape ANSI para definir a cor de fundo de um bloco de texto. `RESET` repõe as cores ao normal.

| Variável  | Cor           | Uso                        |
|-----------|---------------|----------------------------|
| `WALL`    | Cinzento claro | Paredes do labirinto       |
| `PASSAGE` | Preto         | Passagens/corredores       |
| `ENTRY`   | Roxo          | Ponto de entrada           |
| `EXIT`    | Vermelho      | Ponto de saída             |
| `NUMBER`  | Cinzento      | Células que formam o "42"  |

### Forma do "42"

```python
SHAPE_42 = [
    "0010000111",
    "0010000001",
    ...
]
```

Uma matriz de strings onde `"1"` representa um bloco que faz parte do número "42" e `"0"` representa fundo. Esta matriz tem 5 linhas por 10 colunas.

---

## Funções

### `is_42(r, c, start_r, start_c) -> bool`

Verifica se a célula na posição `(r, c)` da grelha faz parte da forma "42", dado o ponto de início da forma em `(start_r, start_c)`.

Calcula a posição relativa da célula dentro da `SHAPE_42` e devolve `True` se o caracter correspondente for `"1"`.

---

### `parse_grid(path: str) -> list[list[int]]`

Lê o ficheiro do labirinto (por defeito `maze.txt`) e converte cada linha de valores hexadecimais numa lista de inteiros.

- Ignora linhas vazias.
- Termina o programa com mensagem de erro se o ficheiro não existir.

**Formato esperado do ficheiro:**
```
f 5 3 a ...
b 0 c 6 ...
```
Cada valor é um hexadecimal de um dígito que representa as paredes de uma célula.

---

### `cell_has_wall(grid, r, c, direction, start_r, start_c) -> bool`

Determina se existe uma parede numa dada `direction` para a célula `(r, c)`.

Lógica de decisão (por prioridade):

1. Se a célula atual faz parte do "42" → **sempre tem parede** (bloco sólido).
2. Se a célula vizinha na direção pedida faz parte do "42" → **também tem parede**.
3. Caso contrário, consulta o **bitmask** da célula no grid para decidir.

---

### `render(grid, entry, exit_) -> str`

A função principal de renderização. Constrói a representação visual do labirinto como uma string com códigos de cor ANSI.

**Processo:**

1. Calcula a posição de início do "42" para o centrar na grelha.
2. Desenha uma **borda superior** completa.
3. Para cada linha `r`:
   - Desenha cada célula com a sua cor (passagem, entrada, saída, ou "42").
   - Desenha a **parede ESTE** (direita) entre células adjacentes.
   - Desenha a **linha de paredes SUL** (baixo) com as quinas de interseção.
4. Devolve todas as linhas unidas com `\n`.

**Cores das células:**
- Célula é parte do "42" → `NUMBER` (cinzento)
- Célula é a entrada → `ENTRY` (roxo)
- Célula é a saída → `EXIT` (vermelho)
- Qualquer outra → `PASSAGE` (preto)

**Conectores entre células "42":** quando duas células "42" adjacentes são separadas por uma parede, o conector (parede partilhada) também recebe a cor `NUMBER` para manter a forma visualmente coesa.

---

### `main() -> None`

Função de orquestração principal:

1. Chama `parse_values()` para ler a configuração (ficheiro `config.txt` ou equivalente).
2. Valida os dados com `is_valid_data()`.
3. Lê o ficheiro do labirinto.
4. Verifica se as dimensões do grid coincidem com `HEIGHT` e `WIDTH` definidos na config.
5. Imprime o labirinto renderizado.

---

### `show_menu() -> None`

Imprime o labirinto e apresenta um menu interativo com as opções disponíveis:

```
1. Re-generate a new maze
2. Show/Hide path
3. Rotate colors
4. Quit
```

---

## Ponto de Entrada

```python
if __name__ == "__main__":
    show_menu()
    while True:
        choice = input("Choice? (1-4): ")
        if choice == '1': ...
        elif choice == '2': ...
        elif choice == '3': ...
        elif choice == '4': break
```

O programa entra num loop infinito a aguardar input do utilizador. As opções 1, 2 e 3 apenas imprimem uma mensagem (funcionalidade por implementar). A opção 4 termina o programa. O bloco `except EOFError` garante que o programa termina graciosamente se o input for fechado (por exemplo, em modo não interativo).

---

## Fluxo Geral

```
config.txt
    │
    ▼
parse_values() ──► is_valid_data()
                        │
                        ▼
                  parse_grid(maze.txt)
                        │
                        ▼
                    render(grid, entry, exit_)
                        │
                        ▼
               Output ANSI no terminal
```

---

## Notas

- O ficheiro `parsing.py` (não incluído) é necessário para que o programa funcione — é responsável por ler `WIDTH`, `HEIGHT`, `ENTRY`, `EXIT` e `OUTPUT_FILE` da configuração.
- As opções do menu (1, 2, 3) estão **por implementar** — apenas imprimem uma mensagem de confirmação.
- O script requer um terminal com suporte a **cores ANSI de 24 bits** (true color) para uma visualização correta.