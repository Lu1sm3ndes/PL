import sys
# Importamos o parser que acabaste de criar
from parser import parser

def run_compiler():
    # Verifica se passaste um ficheiro no terminal
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                conteudo = f.read()
            print(f"--- A iniciar o Parser para: {filename} ---\n")
            
            # MAGIA: Esta linha faz a análise léxica E sintática em simultâneo!
            parser.parse(conteudo)
                
        except FileNotFoundError:
            print(f"Erro: O ficheiro {filename} não foi encontrado.")
    else:
        print(r"Uso: .\.venv\Scripts\python.exe main.py <nome_do_ficheiro.f77>")

if __name__ == "__main__":
    run_compiler()