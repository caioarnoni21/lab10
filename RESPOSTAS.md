# Laboratório 10 — TDD (respostas)

Estrutura: um repositório com três projetos (`ex1`, `ex2`, `ex3`), cada um com
`src/`, `tests/` e `pyproject.toml`. Cada fase do ciclo é um commit `RED:`,
`GREEN:` ou `REFACTOR:`. Os commits `Estrutura:` e `Base:` não são fases (criam
as pastas e trazem o carrinho da teoria).

Testes que **passaram de primeira** foram commitados com prefixo `RED:` e o
sufixo `(passou de primeira)`, para o histórico mostrar onde o ciclo não teve
falha.

Como conferir: `git log --oneline -- ex1` (ou `ex2`, `ex3`) e `bash codespaces.sh`
no Codespace (cobertura + mutmut).

---

## Exercício 1 — Contador de palavras

### a) Ordem da lista (do mais simples ao mais exigente)

| # | Caso | O que obriga o código a fazer |
|---|------|-------------------------------|
| 1 | `""` → `{}` | criar a função e devolver um dict |
| 2 | `"teste"` → `{"teste": 1}` | devolver conteúdo de verdade |
| 3 | `"bom dia"` → 2 itens | separar o texto |
| 4 | `"dia a dia"` → dia 2, a 1 | somar repetições |
| 5 | `"bom\ndia"` → 2 itens | quebra de linha separa |
| 6 | três espaços entre bom e dia → 2 itens | espaços seguidos não criam palavra vazia |
| 7 | `"guarda-chuva"` → 1 item | hífen interno não separa |
| 8 | `"Dia dia DIA"` → `{"dia": 3}` | maiúsculas = minúsculas |
| 9 | `"fim. Fim!"` → `{"fim": 2}` | tirar sinais das bordas |
| 10 | `",dia, ;dia;"` → `{"dia": 2}` | sinais no início e no fim |
| 11 | `":dia: ?dia?"` → `{"dia": 2}` | os outros sinais da lista |
| 12 | `"... !"` → `{}` | palavra que fica vazia depois de tirar os sinais é descartada |

**Por que as duas primeiras posições.** O texto vazio é o caso degenerado: só
obriga a função a existir e a devolver o tipo certo (`return {}`), então o
primeiro passo é o menor possível. `"teste"` é o menor passo seguinte: exige
devolver uma palavra com contagem 1, sem separar nem normalizar nada. Uma
implementação "falsa" (`{texto: 1}`) basta, e o teste 3 a força a generalizar.

O caso 12 fica por último porque só aparece depois que existe remoção de sinais
(o caso 9): antes disso, `"... !"` nem gera palavra vazia.

### b) Desenvolvimento

Ver `ex1/src/contador.py`, `ex1/tests/test_contador.py` e o histórico abaixo.

### c) `git log --oneline -- ex1`

```
e1399da GREEN: descarta o que sobra vazio depois de tirar os sinais
d90ae84 RED: texto so com pontuacao devolve dicionario vazio
4e51840 RED: dois pontos e interrogacao nas bordas (passou de primeira)
7d33952 RED: virgula e ponto e virgula nas bordas (passou de primeira)
66009b5 REFACTOR: separa a normalizacao num gerador e conta com Counter
53e3fb0 GREEN: remove os sinais .,;:!? das bordas
aa91cef RED: ponto e exclamacao no fim sao ignorados
3caca04 GREEN: converte o texto para minusculas
1e42ffa RED: maiusculas contam como minusculas
1a469cf RED: hifen interno faz parte da palavra (passou de primeira)
a4608b7 RED: tres espacos seguidos dao dois itens (passou de primeira)
7673841 RED: quebra de linha separa palavras (passou de primeira)
a5ea554 GREEN: acumula a contagem de cada palavra
418e443 RED: palavra repetida soma ocorrencias
ea3395f GREEN: separa o texto por espacos
320ed11 RED: espaco separa duas palavras
48d2657 GREEN: devolve a unica palavra com contagem 1
8316f51 RED: uma palavra conta uma ocorrencia
7b409c3 GREEN: contar_palavras devolve dicionario vazio
ed0105c RED: texto vazio devolve dicionario vazio
6363145 Remove versao sem historico TDD
fd65000 Remove arquivos .pyc do repositorio
10d48e7 REFACTOR: corrige indentacao do contador
13794ea test do contador
0805301 sr do ex1 contador
```

(os hashes mudam se o repositório for recriado; rode o comando para a versão atual)

**Algum `GREEN:` veio sem um `RED:` antes?** Não. Todo `GREEN:` vem logo depois
de um `RED:` que falhou. O inverso acontece: há `RED:` seguidos sem `GREEN:`
entre eles, que são justamente os testes que passaram de primeira.

### d) Testes que passaram na primeira execução

- `"bom\ndia"`, três espaços entre bom e dia, `"guarda-chuva"`: o GREEN do caso 3 já
  usou `str.split()` sem argumento, que separa por qualquer espaço em branco
  (espaço, `\n`, tabulação), junta espaços seguidos e não mexe no hífen.
- `",dia, ;dia;"` e `":dia: ?dia?"`: o GREEN do caso 9 já usou
  `strip(".,;:!?")` com todos os sinais da especificação, e `strip` age nas
  duas bordas.

**Ficam na suíte?** Sim. Eles não guiaram código, mas documentam partes do
contrato que a especificação cita explicitamente. Se alguém trocar `split()`
por `split(" ")` ou tirar um sinal da lista, são eles que falham. Também
matam mutantes (ex.: `strip` → `lstrip`/`rstrip`).

### e) Cobertura de ramos e mutação

Cobertura (`pytest --cov=src --cov-branch`): **100% de linhas e de ramos**
(8 statements, 4 ramos).

Mutação (`cd ex1 && mutmut run && mutmut results` no Codespace):
**Escore = ____ mortos / ____ total = ____%** ← preencher com a saída

O que eu espero ver vivo (confira com `mutmut show <nome>`):
- `strip(".,;:!?")` → `strip("XX.,;:!?XX")`: **mutante equivalente**. Como o
  texto já passou por `lower()`, nunca existe um `X` maiúsculo para ser
  removido. Nenhum teste consegue matá-lo.
- Se o mutmut trocar `split()` por `rsplit()`, também é equivalente (sem
  `maxsplit` os dois dão o mesmo resultado).

---

## Exercício 2 — Fila de atendimento

### a) Lista de testes (escrita antes do código)

1. Fila nova: `aguardando == 0`
2. Primeira senha normal é `N1`
3. Segunda normal é `N2`
4. Prioritária tem numeração própria: N1, depois `P1`, depois `N2`
5. Tipo desconhecido (`"vip"`) lança `ValueError`
6. `aguardando` conta as senhas emitidas
7. `chamar()` com fila vazia lança `IndexError`
8. `chamar()` devolve a senha e `aguardando` diminui
9. Mesmo tipo segue a ordem de chegada (N1 antes de N2)
10. Prioritária passa na frente (N1, P1 → P1, N1)
11. Depois de 2 prioritárias seguidas, chama a normal que espera
    (N1, P1, P2, P3 → P1, P2, N1, P3)
12. Chamar uma normal zera a sequência
    (N1, N2, P1..P4 → P1, P2, N1, P3, P4, N2)
13. Sem normal esperando, o limite não vale (P1, P2, P3 → P1, P2, P3)
14. Sequência maior que 2 (3 prioritárias sem normal) cede a vez à normal que chega
15. Normal chamada **por falta de prioritária** também zera a sequência

### b) Desenvolvimento

Ver `ex2/src/fila.py`, `ex2/tests/test_fila.py` e `git log --oneline -- ex2`.

### c) Qual teste obrigou a contar? Qual obrigou a zerar?

- **Contar:** o teste 11 (`test_depois_de_duas_prioritarias_chama_uma_normal`).
  Com "prioritária sempre primeiro", ele dava P1, P2, P3, N1. Foi ele que
  criou `_prioritarias_seguidas`.
- **Zerar:** o teste 12 (`test_normal_chamada_zera_a_sequencia_de_prioritarias`).
  Sem zerar, o contador fica em 2 depois de N1 e a fila chama N2 no lugar de
  P3. O teste 11 não pegava isso porque, quando N1 sai, não sobra outra
  normal esperando.

### d) Que teste mostra que o limite de 2 não vale sem normal esperando?

`test_sem_normal_esperando_o_limite_nao_vale`: três prioritárias e nenhuma
normal são chamadas como P1, P2, P3, e não lança erro nem trava. Ele passou de
primeira, porque a condição já era `seguidas >= 2 and normais`. Mesmo assim
fica na suíte, porque documenta a segunda metade da regra
("se houver normal esperando").

### e) mutmut

Cobertura: **100% de linhas e de ramos** (33 statements, 8 ramos).

Escore (preencher com a saída do Codespace): **____ / ____ = ____%**

O que espero ver vivo e o que significa:
- Mutantes nas **mensagens** de erro (`"tipo desconhecido: ..."`,
  `"fila vazia"` → `"XX...XX"`). Os testes só conferem o tipo da exceção, que
  é o que a especificação pede. **Não indicam comportamento da especificação sem
  teste.** Se a mensagem fosse contrato, bastaria `pytest.raises(..., match=...)`.
- `aguardando` é `@property` e `PREFIXOS` / `LIMITE_PRIORITARIAS_SEGUIDAS`
  são constantes de módulo, então o mutmut 3.8.0 **não as muta**. O escore não
  diz nada sobre elas. Por exemplo, trocar o limite para 3 não seria
  detectado pelo mutmut, embora o teste 11 falhasse se alguém fizesse isso à mão.
- Os operadores da regra (`>=` → `>`, `and` → `or`, `+= 1`, `= 0` → `= 1`,
  `not prioritarias`) devem morrer pelos testes 11, 12, 14 e 15. É para isso
  que servem os testes de fronteira que passaram de primeira.

---

## Exercício 3 — Regras novas no carrinho

### a) Testes que contradizem as regras

- **"Cupom em 5000 dá 4500":** pela regra nova, 5000 está abaixo do mínimo de
  10000, então o total é **5000**.
- **"1000 após o cupom dá 900":** subtotal 1000 < 10000, então o total é **1000**.

**O que fazer antes de mudar o código:** reescrever esses testes com o novo
valor esperado (e com um nome que diga a regra), no **primeiro commit `RED:`**
(`156b03b RED: reescreve os testes que contradiziam...`). Não se apagam
testes nem se mexe no código antes. A regra nova muda primeiro o teste. Os
dois mudam juntos porque contradizem a mesma regra: se só um mudasse, o GREEN
quebraria o outro.

Os demais testes da teoria (vazio = 0; 2500; quantidade=2 → 5000; preço 0
rejeitado; "XYZ" rejeitado) continuam válidos.

### b) Uma regra por vez

| Regra | RED | GREEN |
|-------|-----|-------|
| Mínimo 10000 do DEZ | testes reescritos (5000 → 5000; 1000 → 1000) | `if subtotal < 10000: return subtotal` |
| (fronteiras) | 9999 → 9999; 10000 → 9000; cupom antes e mínimo atingido depois | *passou de primeira* |
| Cupom VINTE | 30000 + VINTE → 24000 | cadastra `"VINTE": 20` |
| Mínimo próprio do VINTE | 29999 + VINTE → 29999 | `MINIMOS` por cupom; guarda o código do cupom, calcula no `total` |
| 2º cupom substitui | DEZ→VINTE = 24000; VINTE→DEZ = 27000 | *passou de primeira* (atribuição já substitui) |
| Quantidade ≥ 1 | quantidade 0 → `ValueError` | `if quantidade < 1: raise` |
| (fronteiras) | -1 rejeitada; 1 aceita | *passou de primeira* |
| Quantidade inteira | 1.5, 2.0, "2" → `ValueError` | `if not isinstance(quantidade, int): raise` |

### c) Refactor: porcentagem e mínimo juntos em `CUPONS`

```python
CUPONS = {  # codigo -> (porcentagem de desconto, subtotal minimo)
    "DEZ": (10, 10000),
    "VINTE": (20, 30000),
}
```

**O que mostra que nada mudou:** a suíte inteira (20 testes) continua verde
antes e depois, e o commit `REFACTOR:` **só altera `src/carrinho.py`**
(`git show --stat HEAD -- ex3`). Nenhum teste foi tocado, então o
comportamento verificado é o mesmo. A cobertura de ramos continua em 100%.

### d) Valores de quantidade testados

| Valor | Por quê |
|-------|---------|
| `2` | caso da teoria (multiplica o preço) |
| `1` (explícito) | fronteira válida: o menor valor aceito |
| `0` | fronteira inválida logo abaixo do mínimo, e o teste que guiou o `< 1` |
| `-1` | negativo: confirma que a regra não é só `== 0` |
| `1.5` | não inteiro e ≥ 1: `< 1` sozinho deixaria passar, e é o que guiou o `isinstance` |
| `2.0` | float com valor inteiro: a regra pede *inteira*, e decidi exigir o tipo `int` |
| `"2"` | string: sem a checagem de tipo daria `TypeError`, não o `ValueError` pedido |

O teste parametrizado também confere que o subtotal **não muda** quando a
quantidade é rejeitada. Fora da lista: `True`/`False` (`bool` é subclasse de
`int` no Python), que seria a próxima pergunta para a especificação.

---

## Síntese

- O `git log` mostra o ciclo: todo `GREEN:` tem um `RED:` imediatamente antes.
- Testes que passam de primeira não guiaram código, mas ficam porque
  documentam fronteiras do contrato e matam mutantes.
- Regra nova: muda primeiro o teste (ex3, commit `RED: reescreve...`), depois
  o código.
- A cobertura deu 100% nos três projetos, mas o mutmut mostra que isso não
  basta: constantes, `@property` e mensagens ficam fora ou sobrevivem.
