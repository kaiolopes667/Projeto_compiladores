from parser import parser
from generator import gerar_codigo

arquivo_entrada = "exemplo.turtle"
print(f"Lendo o arquivo fixo: {arquivo_entrada}")

try:
    with open(arquivo_entrada, "r") as f:
        codigo = f.read()
except FileNotFoundError:
    print(f"Arquivo '{arquivo_entrada}' não encontrado.")
    exit(1)

resultado = parser.parse(codigo)

if resultado:
    gerar_codigo(resultado)
    print("Código gerado em 'saida.py'")
else:
    print("Erro na compilação.")
