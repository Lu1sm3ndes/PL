import sys
import os
from parser import parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer  
from compiler import Compiler

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
                    continue 
                print(f"{indent}    |-- {key}: ", end="")
                if isinstance(value, list) or hasattr(value, '__dict__'):
                    print() 
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
            
            # --- ETAPA 1 e 2: Análise Léxica, Sintática e AST ---
            ast = parser.parse(conteudo)
            
            if ast:
                print("🌳 Árvore Sintática Abstrata (Original):")
                print_ast(ast)
                print("\n" + "="*50 + "\n")

                # --- ETAPA 3: Análise Semântica ---
                analisador = SemanticAnalyzer()
                
                # A CORREÇÃO MAGNÍFICA ESTÁ AQUI: Desempacotar a tupla!
                erros, avisos = analisador.analyze(ast)
                
                if avisos:
                    print("⚠️ Avisos Semânticos:")
                    for aviso in avisos:
                        print(f"  - {aviso}")

                if erros:
                    print("\n❌ Erros Semânticos Encontrados:")
                    for erro in erros:
                        print(f"  - {erro}")
                else:
                    print("\n✅ Análise Semântica BEM SUCEDIDA!")
                    
                    # --- ETAPA 4: Otimização (Valorização) ---
                    print("\n--- A Otimizar a Árvore (Constant Folding & Dead Code) ---")
                    otimizador = Optimizer()
                    ast = otimizador.optimize(ast)
                    
                    print("🌳 Árvore Sintática (Otimizada):")
                    print_ast(ast)
                    print("\n✨ Otimização concluída.")

                    # --- ETAPA 5: Geração de Código VM ---
                    compilador_vm = Compiler(analisador.symbol_table)
                    codigo_gerado = compilador_vm.compile(ast)
                    
                    nome_base = os.path.basename(filename)
                    nome_vm = nome_base.replace('.f77', '.vm')
                    
                    pasta_origem = os.path.dirname(filename) or "."
                    pasta_destino = os.path.join(pasta_origem, "vm")
                    
                    if not os.path.exists(pasta_destino):
                        os.makedirs(pasta_destino)
                        
                    out_file = os.path.join(pasta_destino, nome_vm)
                    
                    with open(out_file, 'w') as f:
                        for linha in codigo_gerado:
                            f.write(linha + '\n')
                            
                    print(f"\n💾 Código guardado com sucesso em: {out_file}")
                    print(f"🚀 Abre a Máquina Virtual EWVM, cola o código e clica 'Run'!")
            else:
                print("⚠️ O parser não devolveu nenhuma estrutura.")
                
        except FileNotFoundError:
            print(f"Erro: O ficheiro {filename} não foi encontrado.")
    else:
        print(r"Uso: python main.py <nome_do_ficheiro.f77>")

if __name__ == "__main__":
    run_compiler()