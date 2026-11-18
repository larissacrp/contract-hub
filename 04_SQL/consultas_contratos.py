
import sqlite3
import pandas as pd
from pathlib import Path


pasta_projeto = Path(__file__).resolve().parent.parent


caminho_banco = pasta_projeto / "04_SQL" / "banco_contratos.db"


conexao = sqlite3.connect(caminho_banco)


consulta = """
SELECT
    Status_Contrato,
    COUNT(*) AS Quantidade
FROM contratos
GROUP BY Status_Contrato
"""


resultado = pd.read_sql_query(consulta, conexao)


print("\nCONTRATOS POR STATUS:")
print(resultado)

consulta_renovacao = """
SELECT
    COUNT(*) AS Total_Renovacao_Automatica
FROM contratos
WHERE Renovacao_Automatica = 'Sim'
"""

resultado_renovacao = pd.read_sql_query(
    consulta_renovacao,
    conexao
)

print("\nCONTRATOS COM RENOVAÇÃO AUTOMÁTICA:")
print(resultado_renovacao)

consulta_vencimentos = """
SELECT
    COUNT(CASE
        WHEN Dias_Restantes_Vencimento BETWEEN 0 AND 30
        THEN 1
    END) AS Vencem_30_Dias,

    COUNT(CASE
        WHEN Dias_Restantes_Vencimento BETWEEN 0 AND 60
        THEN 1
    END) AS Vencem_60_Dias,

    COUNT(CASE
        WHEN Dias_Restantes_Vencimento BETWEEN 0 AND 90
        THEN 1
    END) AS Vencem_90_Dias

FROM contratos
WHERE Status_Contrato = 'Ativo'
"""
resultado_vencimentos = pd.read_sql_query(
    consulta_vencimentos,
    conexao
)

print("\nCONTRATOS ATIVOS PRÓXIMOS DO VENCIMENTO:")
print(resultado_vencimentos.to_string(index=False))

consulta_detalhes = """
SELECT
    ID_Contrato,
    Cliente,
    Tipo_Servico,
    Data_Termino_Vigencia,
    Dias_Restantes_Vencimento,
    Tipo_Renovacao,
    Renovacao_Automatica

FROM contratos

WHERE Status_Contrato = 'Ativo'
AND Dias_Restantes_Vencimento BETWEEN 0 AND 30

ORDER BY Dias_Restantes_Vencimento ASC
"""

resultado_detalhes = pd.read_sql_query(
    consulta_detalhes,
    conexao
)

print("\nCONTRATOS QUE VENCEM EM ATÉ 30 DIAS:")
print(resultado_detalhes.to_string(index=False))


pasta_resultados = pasta_projeto / "02_Bases_Tratadas"

arquivo_csv = pasta_resultados / "contratos_vencimento_30_dias.csv"

resultado_detalhes.to_csv(
    arquivo_csv,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print("\nArquivo CSV exportado com sucesso!")
print("Total de contratos exportados:", len(resultado_detalhes))
print("Local:", arquivo_csv)

consulta_completa = """
SELECT *
FROM contratos
"""

base_completa = pd.read_sql_query(
    consulta_completa,
    conexao
)
arquivo_completo = (
    pasta_projeto
    / "02_Bases_Tratadas"
    / "contratos_dashboard.csv"
)

base_completa.to_csv(
    arquivo_completo,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)
print("\nBASE COMPLETA EXPORTADA:")
print("Total de contratos:", len(base_completa))
print("Total de colunas:", len(base_completa.columns))
print("Arquivo:", arquivo_completo)

conexao.close()
