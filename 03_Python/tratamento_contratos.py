import pandas as pd
from pathlib import Path

pasta_projeto = Path(__file__).resolve().parent.parent

caminho_arquivo = pasta_projeto / "01_Bases_Originais" / "base_contratos.xlsx"

df = pd.read_excel(caminho_arquivo, sheet_name="BASE GERAL")
print(df.head())

print("Quantidade de contratos:", df.shape[0])
print("Quantidade de colunas:", df.shape[1])


print("\nNOMES DAS COLUNAS:")
print(df.columns.tolist())

print("\nVALORES VAZIOS POR COLUNA:")
print(df.isnull().sum())

print("\nTIPOS DE DADOS:")
print(df.dtypes)


df= df.drop(columns=["Unnamed: 20",
"DATA_REFERENCIA"])

print("\nBASE APÓS REMOVER COLUNAS AUXILIARES:")
print("Quantidade de contratos:", df.shape[0])
print("Quantidade de colunas:", df.shape[1])

print(df.head())


pasta_destino = pasta_projeto/"02_Bases_Tratadas"

pasta_destino.mkdir(parents=True, exist_ok=True)

arquivo_saida = pasta_destino / "contratos_tratados.xlsx"

df.to_excel(arquivo_saida, index=False)

print("\nBase tratada salva com sucesso!")
print("Local:", arquivo_saida)

duplicados = df["ID_Contrato"].duplicated().sum()

print("\nCONTRATOS DUPLICADOS:")
print(duplicados)

sem_id = df['ID_Contrato'].isnull().sum()

print("\nCONTRATOS SEM ID:")
print(sem_id)

datas_invalidas = (
    df["Data_Termino_Vigencia"]
    < df["Data_Inicio_Vigencia"]
).sum()

print("\nCONTRATOS COM DATAS INCONSISTENTES:")
print(datas_invalidas)




multa_inconsistente = df[
    (df["Possui_Multa"] == "Não") &
    (df["Valor_Multa"].notna())
]

print("\nCONTRATOS SEM MULTA, MAS COM VALOR:")
print(len(multa_inconsistente))



multa_sem_valor = df[
    (df["Possui_Multa"] == "Sim") &
    (df["Valor_Multa"].isna())
]

print("\nCONTRATOS COM MULTA, MAS SEM VALOR:")
print(len(multa_sem_valor))


aditivo_inconsistente = df[
    (df["Possui_Aditivo"] == "Não") &
    (df["Data_Ultimo_Aditivo"].notna())
]

print("\nCONTRATOS SEM ADITIVO, MAS COM DATA:")
print(len(aditivo_inconsistente))



aditivo_sem_data = df[
    (df["Possui_Aditivo"] == "Sim") &
    (df["Data_Ultimo_Aditivo"].isna())
]

print("\nCONTRATOS COM ADITIVO, MAS SEM DATA:")
print(len(aditivo_sem_data))


contratos_por_status = df["Status_Contrato"].value_counts()

print("\nCONTRATOS POR STATUS:")
print(contratos_por_status)

renovacao_automatica = (
    df["Renovacao_Automatica"] == "Sim"
).sum()

print("\nCONTRATOS COM RENOVAÇÃO AUTOMÁTICA:")
print(renovacao_automatica)


contratos_com_sla = df["SLA_Contratual"].notna().sum()

print("\nCONTRATOS COM SLA:")
print(contratos_com_sla)