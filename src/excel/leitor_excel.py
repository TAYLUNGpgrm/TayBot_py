import pandas as pd
from config import CAMINHO_PLANILHA

def ler_planilha(caminho=CAMINHO_PLANILHA):
    try:
        df = pd.read_excel(
            caminho,
            dtype={
                "Usuario": str,
                "Senha": str,
                "CNPJ": str,               # Empresa emissora (mantido)
                "CpfCnpjTomador": str,     # Cliente (CPF ou CNPJ)
                "NomeTomador": str,
                "CEP": str,
                "Logradouro": str,
                "Numero": str,
                "Complemento": str,
                "Bairro": str,
                "Municipio": str,
                "UF": str,
                "DescricaoServico": str,
                "CTISS": str,
                "ItemServico": str,
                "NaturezaOperacao": str,
                "RegimeTributacao": str,
                "MunicipioIncidencia": str,
                "Valor": str
            }
        )
        print(f"[SUCESSO] Planilha lida com {len(df)} linhas.")
        return df
    except Exception as e:
        print(f"[ERRO] Falha ao ler planilha: {e}")
        return pd.DataFrame()