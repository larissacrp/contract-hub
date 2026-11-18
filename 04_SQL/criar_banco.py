import pandas as pd
import sqlite3
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent

arquivo_excel = pasta_projeto / "02_Bases_Tratadas" / "contratos_tratados.xlsx"

df = pd.read_excel(arquivo_excel)   

caminho_banco = pasta_projeto / "04_SQL" / "banco_contratos.db"

conexao = sqlite3.connect(caminho_banco)

df.to_sql("contratos", conexao, if_exists="replace", index=False)

resultado = pd.read_sql_query(
    "SELECT COUNT(*) AS total_contratos FROM contratos", conexao
)

print("\nCONTRATOS NO BANCO DE DADOS:")
print(resultado)

conexao.close() 
print("\nBanco de dados criado com sucesso!")