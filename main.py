from tokenizer import tokenize
from parser import parser
from semantic import analisar_semantica
from generator import gerar_codigo
import sys

if len(sys.argv) < 3:
    print("Uso: python main.py <entrada.txt> <saida.py>")
    exit(1)

arquivo_entrada = sys.argv[1]
arquivo_saida = sys.argv[2]

print(f"Lendo o arquivo: {arquivo_entrada}")

try:
    with open(arquivo_entrada, "r") as f:
        codigo = f.read()
except FileNotFoundError:
    print(f"Arquivo '{arquivo_entrada}' não encontrado.")
    exit(1)

try:
    tokens = tokenize(codigo)
    print("Análise léxica OK")
except Exception as e:
    print(f"Erro léxico: {e}")
    exit(1)

try:
    ast = parser(tokens)
    print("Análise sintática OK")
except Exception as e:
    print(f"Erro sintático: {e}")
    exit(1)

try:
    analisar_semantica(ast)
    print("Análise semântica OK")
except Exception as e:
    print(f"Erro semântico: {e}")
    exit(1)

gerar_codigo(ast, saida=arquivo_saida)
print(f"Código gerado em '{arquivo_saida}'")
