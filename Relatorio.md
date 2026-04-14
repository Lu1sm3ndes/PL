# Relatório Técnico: Compilador Fortran 77

**Unidade Curricular:** Processamento de Linguagens  
**Autores:**

---

## 1. Instruções de Execução (Como correr o compilador)

Para testar a Análise Léxica e Sintática do nosso compilador, é necessário ter o Python e a biblioteca PLY instalados.

**Passos:**

1. Instalar dependências: `pip install ply`
2. Na raiz do projeto, executar o analisador passando o ficheiro de teste como argumento:
   `python main.py testes/ex3_primo.f77`

---

## 2. Opções de Implementação

Para a construção deste projeto, optámos pela utilização da linguagem **Python** em conjunto com a ferramenta **PLY (Python Lex-Yacc)**.
A arquitetura foi dividida de forma modular:

- `lexer.py`: Responsável por tokenizar o código (Expressões Regulares).
- `parser.py`: Responsável por validar a estrutura sintática.
- `main.py`: Ponto de entrada que interliga os módulos e lê os ficheiros de input.

_(Aqui podem falar sobre os tokens de valorização que já incluíram, como FUNCTION e RETURN)._

---

## 3. Gramática Utilizada

A nossa gramática Livre de Contexto foi desenhada para suportar a estrutura do Fortran 77.
De forma resumida, a estrutura base do programa foi definida como:

- **Programa:** `PROGRAM IDEN` seguido de Declarações, Instruções e `END`.
- **Declarações:** Suporta `INTEGER`, `REAL`, `LOGICAL` e declaração de Arrays (ex: `NUMS(5)`).
- **Instruções:** Suporta atribuições, leitura (`READ`), escrita (`PRINT`), ciclos (`DO ... CONTINUE`) e estruturas condicionais (`IF ... THEN ... ELSE ... ENDIF`).
- **Precedência:** Foi definida a precedência de operadores para garantir a correta avaliação matemática (Multiplicação/Divisão antes da Soma/Subtração).

---

## 4. Dificuldades Encontradas

Durante o desenvolvimento, a equipa deparou-se com alguns desafios técnicos:

1. **Operadores Relacionais e Lógicos:** O Fortran utiliza pontos nos operadores (ex: `.EQ.`, `.AND.`). Foi necessário ajustar as expressões regulares no Lexer para garantir que estes não eram confundidos com chamadas de métodos ou identificadores normais.
2. **A instrução PRINT:** Inicialmente, a gramática não suportava a mistura de _strings_ e variáveis na mesma instrução de impressão (ex: `PRINT *, 'Valor:', N`). O problema foi resolvido criando uma regra genérica `elemento_print` que aceita ambas as tipologias de forma alternada.

---

## 5. Resultados dos Testes

Para comprovar a robustez do nosso analisador sintático, submetemos os ficheiros de teste mais complexos fornecidos no enunciado (Exemplo 4 com _arrays_ e Exemplo 5 com subprogramas).

Como se pode observar na imagem abaixo, o compilador reconheceu a estrutura na íntegra sem emitir qualquer erro de sintaxe:

![Resultado da Compilação - Exemplos 4 e 5](print_ex5.png)
