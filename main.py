import sys
import os
from parser import parser

# Função para desenhar a árvore 🌳
def print_ast(node, indent=""):
    if isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    elif hasattr(node, '__dict__'):
        label = f" [Label: {node.label}]" if getattr(node, 'label', None) else ""
        print(f"{indent}└── {node.__class__.__name__}{label}")
        for key, value in node.__dict__.items():
            if key != 'label' and value is not None:
                if isinstance(value, list) and len(value) == 0:
                    continue # Esconde listas vazias para ficar mais limpo
                print(f"{indent}    |-- {key}: ", end="")
                if isinstance(value, list) or hasattr(value, '__dict__'):
                    print() # Quebra a linha
                    print_ast(value, indent + "        ")
                else:
                    print(value)
    else:
        print(f"{indent}└── {node}")

def run_compiler():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                conteudo = f.read()
            print(f"--- A iniciar o Compilador para: {filename} ---\n")
            
            # --- ETAPA 1 e 2: Análise Léxica, Sintática e Construção da AST ---
            ast = parser.parse(conteudo)
            
            if ast:
                print("🏆 AST CONSTRUÍDA COM SUCESSO!\n")
                print("Estrutura da Árvore de Sintaxe Abstrata:")
                print_ast(ast)
                
                # --- ETAPA 3: ANÁLISE SEMÂNTICA ---
                from semantic import SemanticAnalyzer
                
                print("\n--- A iniciar Análise Semântica ---")
                analisador = SemanticAnalyzer()
                erros_semanticos = analisador.analyze(ast)
                
                if erros_semanticos:
                    print("\n⚠️ O código tem falhas de lógica (Semântica):")
                    for erro in erros_semanticos:
                        print(erro)
                else:
                    print("✅ Análise Semântica BEM SUCEDIDA: Tipos e variáveis validados a 100%!")
                    
                    # --- NOVA ETAPA: OTIMIZAÇÃO DA AST ---
                    from optimizer import Optimizer
                    
                    print("\n--- A otimizar a Árvore de Sintaxe (AST) ---")
                    otimizador = Optimizer()
                    ast = otimizador.optimize(ast)
                    print("⚡ Otimização concluída: Constant Folding e Eliminação de Código Morto aplicados!")
                    
                    # Se quiseres ver a árvore otimizada no terminal para comparar, descomenta as 2 linhas abaixo:
                    # print("\nEstrutura da Árvore Otimizada:")
                    # print_ast(ast)
                    
                    # --- ETAPA 4: GERAÇÃO DE CÓDIGO (EWVM) ---
                    from compiler import Compiler
                    
                    print("\n--- A gerar código para a Máquina Virtual (EWVM) ---")
                    compilador_vm = Compiler(analisador.symbol_table)
                    codigo_gerado = compilador_vm.compile(ast)
                    
                    # --- LÓGICA DE ORGANIZAÇÃO DE FICHEIROS ---
                    nome_base = os.path.basename(filename) # Ex: "ex5_conversor.f77"
                    nome_vm = nome_base.replace('.f77', '.vm') # Ex: "ex5_conversor.vm"
                    
                    # Descobre a pasta onde está o ficheiro original (ex: "testes")
                    pasta_origem = os.path.dirname(filename)
                    if not pasta_origem: pasta_origem = "."
                    
                    # Define a pasta de destino (ex: "testes/vm")
                    pasta_destino = os.path.join(pasta_origem, "vm")
                    
                    # Cria a pasta 'vm' se não existir
                    if not os.path.exists(pasta_destino):
                        os.makedirs(pasta_destino)
                        
                    out_file = os.path.join(pasta_destino, nome_vm)
                    
                    with open(out_file, 'w') as f:
                        for linha in codigo_gerado:
                            f.write(linha + '\n')
                            
                    print(f"💾 Código guardado com sucesso em: {out_file}")
                    print(f"🚀 Abre a Máquina Virtual EWVM, cola o código e clica 'Run'!\n")
                    
            else:
                print("⚠️ O parser não devolveu nenhuma estrutura.")
                
        except FileNotFoundError:
            print(f"Erro: O ficheiro {filename} não foi encontrado.")
    else:
        print(r"Uso: python main.py <nome_do_ficheiro.f77>")

if __name__ == "__main__":
    run_compiler()