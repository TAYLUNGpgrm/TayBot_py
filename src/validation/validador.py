import pandas as pd
import re
from steps.etapa_leitura import executar_leitura
from steps.etapa_automacao import executar_bot

def validar_dados(df):
    erros = []

    for index, linha in df.iterrows():
        cnpj = str(linha.get("CNPJ", "")).strip()
        nome = str(linha.get("Nome", "")).strip()

        # Validação de campos obrigatórios
        if not cnpj or not nome:
            erros.append((index, "CNPJ ou Nome vazio"))
            continue

        # Validação de CNPJ
        if not re.match(r"^\d{14}$", cnpj):
            erros.append((index, f"CNPJ inválido: {cnpj}"))

        # Validação de duplicidade
        if df["CNPJ"].duplicated().iloc[index]:
            erros.append((index, f"CNPJ duplicado: {cnpj}"))

    return erros

def main():
    df = executar_leitura()
    erros = validar_dados(df)

    if erros:
        print("[ERROS DE VALIDAÇÃO]")
        for linha, motivo in erros:
            print(f"Linha {linha}: {motivo}")
    else:
        executar_bot(df)