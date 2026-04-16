# Compilador Fortran 77 - PL 2026

Este repositório contém o código-fonte de um compilador para a linguagem **Fortran 77** (standard ANSI X3.9-1978), desenvolvido para a Unidade Curricular de **Processamento de Linguagens**.

O sistema realiza a tradução de código Fortran para instruções da **EWVM (Experimental Web Virtual Machine)**, passando por fases de análise léxica, sintática, semântica e otimização intermédia da árvore de sintaxe.

## Funcionalidades e Estrutura

- **Pipeline Completa:** Integração de Lexer, Parser, Analisador Semântico, Otimizador e Gerador de Código [cite: 39-44].
- **Análise Semântica (Fiscal de Tipos):** Validação rigorosa de tipos, declaração de variáveis e tipagem implícita (letras I-N).
- **Otimização (Valorização):** Implementação de _Constant Folding_ e _Dead Code Elimination_ para gerar código máquina mais eficiente.
- **Subprogramas:** Suporte integral a `FUNCTION` e `SUBROUTINE` com isolamento de contextos e passagem de parâmetros.
- **Gestão de Arrays:** Alocação de memória no _Heap_ via `alloc` e acesso estruturado a vetores.

- `lexer.py`: Especificação de tokens e análise léxica.
- `parser.py`: Gramática e construção da Árvore de Sintaxe Abstrata (AST).
- `ast_nodes.py`: Definição das classes dos nós da AST.
- `semantic.py`: Analisador semântico baseado no padrão _Visitor_.
- `optimizer.py`: Módulo de otimização intermédia[cite: 71].
- `compiler.py`: Tradução da AST para código máquina EWVM.
- `main.py`: Ponto de entrada do compilador.
- `testes/`: Diretório com os exemplos oficiais e suite de testes de erro.

<div style="page-break-after: always;"></div>

### Pré-requisitos

- Python 3.10 ou superior.
- Biblioteca PLY instalada:

```bash
pip install ply
```

Para compilar um ficheiro Fortran, execute o `main.py` passando o caminho do ficheiro como argumento:

```bash
python main.py testes/ex3_primo.f77
```

Nota: O código gerado (.vm) será guardado automaticamente na pasta testes/../.

### Testes

O projeto inclui os 5 exemplos oficiais do guião e testes adicionais de robustez:

- `ex1_hello.f77`: Teste base de I/O.

- `ex5_conversor.f77`: Teste complexo de subprogramas e ciclos.

- `teste_otimizacao.f77`: Validação das técnicas de otimização intermédia.

- `erro_semantico.f77` e `erro_sintatico.f77`: Testes de interceção de erros de tipos.

- `ciclos_aninhados.f77`: Teste de controlo de fluxo avançado com ciclos `DO` sobrepostos, garantindo a correta gestão de etiquetas de salto e isolamento de contadores.

- `fibonacci.f77`: Validação de algoritmos iterativos complexos, testando a reatribuição sucessiva de variáveis e a acumulação de valores em memória.

- `logica_bool.f77`: Teste integral aos operadores relacionais (`.GE.`, `.LT.`, `.AND.`) e à correta avaliação de precedências na Árvore de Sintaxe Abstrata (AST).

- `par_impar.f77`: Teste funcional simples utilizando a função intrínseca `MOD` e estruturas condicionais `IF-THEN-ELSE` para validação de lógica modular.

### Autores

António Luís Braga Mendes - A84675

[Nome 2] - [Número]

[Nome 3] - [Número]

Projeto realizado para a Unidade Curricular de Processamento de Linguagens - 2026.

---
