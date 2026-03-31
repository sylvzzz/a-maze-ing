Boa pergunta! Aqui está um roadmap claro do que estudar e por onde começar:

---

## 🗺️ Roadmap — Maze Generator & Solver em Python (ASCII Terminal)

---

### 1. Parsing do Config File
**O que ver:** `open()`, `str.strip()`, `str.partition()`, `str.startswith()`
**Conceitos:** ler ficheiro linha a linha, ignorar comentários (`#`), separar `KEY=VALUE`, tratar erros com `try/except` e exceções customizadas (`class ConfigError(Exception)`)

---

### 2. Validação dos Parâmetros
**O que ver:** type casting (`int()`, `bool()`), condições de validação
**Conceitos:** verificar que WIDTH/HEIGHT são inteiros positivos, que ENTRY/EXIT estão dentro dos limites da grelha, que PERFECT é `True` ou `False`

---

### 3. Estrutura de Dados do Maze
**O que ver:** listas 2D em Python (`[[...] for _ in range(n)]`), dicionários, conjuntos (`set`)
**Conceitos:** representar o labirinto como uma grelha de células, cada célula com paredes (Norte, Sul, Este, Oeste)

---

### 4. Geração do Maze
**O que ver:** algoritmos de geração de labirintos
**Conceitos a pesquisar:**
- **Recursive Backtracker (DFS)** — mais simples, bom ponto de partida
- **Kruskal's / Prim's** — para mazes perfeitos alternativos
- A diferença entre **maze perfeito** (sem ciclos, sempre há caminho único) e **imperfeito**

---

### 5. Representação ASCII
**O que ver:** `print()`, strings com `+`, `join()`, caracteres como `█`, `|`, `-`, `+`, ` `
**Conceitos:** converter a grelha de células+paredes para linhas de texto, linha a linha, célula a célula — é aqui que entra o teu trabalho principal

---

### 6. Output para Ficheiro
**O que ver:** `open()` com modo `"w"`, `file.write()`
**Conceitos:** escrever o maze em ASCII para o ficheiro definido em `OUTPUT_FILE`

---

### 7. Resolução do Maze
**O que ver:** algoritmos de pathfinding
**Conceitos a pesquisar:**
- **BFS (Breadth-First Search)** — garante caminho mais curto, fácil de implementar
- **DFS** — mais simples mas não garante caminho ótimo
- Marcar o caminho solução no ASCII (ex: com `·` ou `*`)

---

### 8. Display no Terminal
**O que ver:** `os.system('clear')`, biblioteca `colorama` (opcional, para cores)
**Conceitos:** imprimir o maze limpo no terminal, destacar ENTRY, EXIT e solução

---

## 📌 Por onde começar?

```
1. config parser  →  2. validação  →  3. estrutura da grelha
       →  4. geração (DFS)  →  5. render ASCII  →  6. output ficheiro
```

Começa pelo **passo 1 e 2** — são independentes e dão-te a base. Depois o **passo 3 e 5** juntos, porque a forma como representas o maze em memória define diretamente como o renderizas em ASCII.

---

**Dica principal:** pesquisa *"recursive backtracker maze python"* e *"maze ASCII representation python"* — há muitos exemplos visuais que tornam os conceitos muito mais claros.